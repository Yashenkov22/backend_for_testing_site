from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'category', 'created_at', 'updated_at')


class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'test')
    inlines = [AnswerInLine]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'is_correct')