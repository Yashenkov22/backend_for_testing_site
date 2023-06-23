from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .models import Category, Test, Question, Answer



def home_page(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request,
                  'tests/home.html',
                  context=context)


def category_page(request, cat_id):
    category = Category.objects.get(pk=cat_id)
    context = {
        'category': category
    }
    return render(request,
                  'tests/category_page.html',
                  context=context)


def test_page(request, cat_id, test_id):
    test = Test.objects.get(pk=test_id)
    done = request.session.get(f'test{test_id}')
    return render(request, 'tests/test_page.html', context={'test': test,
                                                            'done': done,
                                                            'cat_id': cat_id})


@login_required
def question_page(request: HttpRequest, cat_id, test_id, quest_id):
    if request.method == 'POST':
        answer = request.POST.get(f'question{quest_id}')
        if not answer:
            notice = 'Выберите ответ'
            question = Question.objects.get(pk=quest_id)
            return render(request, 'tests/question_page.html', context={'question': question,
                                                                        'notice': notice})
        request.session['user_answers'].append(answer)
        right_answer = Answer.objects.filter(question=quest_id).get(is_correct=True)
        request.session['right_answers'].append(right_answer.answer)
        request.session.modified = True
        quest_id += 1
        try:
            question = Question.objects.get(pk=quest_id)
        except ObjectDoesNotExist:
            return redirect(reverse('test_results', kwargs={'cat_id': cat_id,
                                                            'test_id': test_id}))
        else:
            return redirect(question.get_absolute_url())
    else:
        if quest_id == 1:
            request.session['user_answers'] = []
            request.session['right_answers'] = []
        question = Question.objects.get(pk=quest_id)
    return render(request,
                  'tests/question_page.html',
                  context={'question': question})


@login_required
def test_results(request, cat_id, test_id):
    test = Test.objects.get(pk=test_id)
    user_answers = request.session['user_answers']
    right_answers = request.session['right_answers']
    correct = sum(1 for x,y in zip(user_answers, right_answers) if x == y)
    uncorrect = len(user_answers) - correct
    procents = round(correct / len(user_answers), 2) * 100
    if not request.session.get(f'test{test_id}'):
        request.session[f'test{test_id}'] = True

    context = {
        'test' : test,
        'user_answers': user_answers,
        'correct': correct,
        'uncorrect': uncorrect,
        'procents': procents,
    }
    return render(request,
                  'tests/test_results.html',
                  context=context)