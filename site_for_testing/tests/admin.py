from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from django.contrib import admin
from django import forms

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'category', 'created_at', 'updated_at')


class BaseAnswerFormSet(BaseInlineFormSet):
    def clean(self):
        is_correct = 0
        for form in self.forms:
            if form.cleaned_data.get('is_correct'):
                is_correct += 1
        if is_correct > 1:
            raise ValidationError('Нельзя установить более одного верного ответа')
        if is_correct == 0:
            raise ValidationError('Нужно выбрать один правильный ответ!')

AnswerFormSet = inlineformset_factory(parent_model=Question,
                                      model=Answer,
                                      formset=BaseAnswerFormSet,
                                      fields = ('answer', 'is_correct', 'question'))


class AnswerInLine(admin.TabularInline):
    model = Answer
    formset = AnswerFormSet
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'test')
    inlines = [AnswerInLine]


# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     form = AnswerForm
#     list_display = ('answer', 'is_correct')