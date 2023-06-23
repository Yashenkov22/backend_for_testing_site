from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})


class Test(models.Model):
    class Level(models.TextChoices):
        EAZY = ('eazy', 'Легко')
        MEDIUM = ('medium', 'Средне')
        HARD = ('hard', 'Сложно')

    name = models.CharField('Название', max_length=100)
    level = models.CharField('Сложность',
                            max_length=6,
                            choices=Level.choices,
                            default=Level.EAZY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,
                                 related_name='tests',
                                 on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('test_page', kwargs={'cat_id': self.category.id,
                                            'test_id': self.pk})


class Question(models.Model):
    name = models.CharField('Название', max_length=100)
    question = models.TextField('Описание')
    test = models.ForeignKey(Test,
                             related_name='questions',
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('question_page', kwargs={'cat_id': self.test.category.pk,
                                                'test_id': self.test.pk,
                                                'quest_id': self.pk})

class Answer(models.Model):
    answer = models.CharField('Ответ', max_length=255)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question,
                                 related_name='answers',
                                 on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f'Вопрос {self.pk}'