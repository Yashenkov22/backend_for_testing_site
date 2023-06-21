from django.contrib import admin
from .models import *
from django import forms
from django.core.exceptions import ValidationError


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'category', 'created_at', 'updated_at')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer', 'is_correct', 'question')

    def clean(self):
        cleaned_data = super().clean()
        is_correct = cleaned_data.get('is_correct')
        print('ответ')
        answers = Answer.objects.filter(question=cleaned_data.get('question'))
        print(len(answers))
        if is_correct:
            # Проверяем, что у других ответов не установлен чекбокс "Верный ответ"
            print('ятут')
            for answer in answers:
                if answer.is_correct and answer.answer != cleaned_data.get('answer'):
                    raise ValidationError("Нельзя установить более одного верного ответа")
        return cleaned_data


class AnswerInLine(admin.TabularInline):
    form = AnswerForm
    model = Answer
    extra = 1
    fields = ('answer', 'is_correct', 'question')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'test')
    inlines = [AnswerInLine]


# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     form = AnswerForm
#     list_display = ('answer', 'is_correct')