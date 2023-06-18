from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Category, Test, Question
from django.http import HttpRequest


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
    tests = Test.objects.filter(category=category)
    context = {
        'category': category,
        'tests': tests
    }
    return render(request,
                  'tests/category.html',
                  context=context)

def test_page(request, cat_id, test_id):
    test = Test.objects.get(pk=test_id)
    return render(request, 'tests/test_page.html', context={'test': test})

def question_page(request: HttpRequest, cat_id, test_id, quest_id):
    if request.method == 'POST':
        answer = request.POST.get(f'question{quest_id}')
        request.session['answers'][f'question{quest_id}'] = answer
        request.session.modified = True
        print(request.session['answers'])
        quest_id += 1
        try:
            question = Question.objects.get(pk=quest_id)
        except ObjectDoesNotExist:
            test = Test.objects.get(pk=test_id)
            answers = list(request.session['answers'].values())
            correct = len([ans for ans in answers if ans == 'True'])
            uncorrect = len(answers) - correct
            procents = round(correct / len(answers), 2) * 100
            context = {
                'test': test,
                'answers': answers,
                'correct': correct,
                'uncorrect': uncorrect,
                'procents': procents,
            }
            return render(request, 'tests/test_results.html', context=context)
        else:
            return redirect(question.get_absolute_url())
    else:
        if quest_id == 1:
            request.session['answers'] = {}
        print(request.session['answers'])
        question = Question.objects.get(pk=quest_id)
    return render(request, 'tests/question_page.html', context={'question': question})