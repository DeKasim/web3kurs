from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from simple_history.models import HistoricalRecords

class Topic(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                r'[0-9a-zA-Za-яA-Я -]',
                'В названии темы допустимы только буквы и цифры')
        ])
    picture = models.ImageField(upload_to="topic_pictures", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

class Question(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Заголовок',
        validators=[
            RegexValidator(
                r'[0-9a-zA-Za-яA-Я ?,.-]',
                'В названии вопроса допустимы буквы, цифры, пробелы, и знаки препинания')
        ])
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='Тема')
    question_text = models.TextField(verbose_name='Содержимое')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.title} - {self.author}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    answer_text = models.TextField(max_length=200, verbose_name='Содержимое')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    history = HistoricalRecords()

    def likes_count(self):
        return self.likes.all().count()

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class Comment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    comment_text = models.TextField(max_length=200, verbose_name='Содержимое')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    history = HistoricalRecords()

    def likes_count(self):
        return self.likes.all().count()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ', related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Лайк на ответ'
        verbose_name_plural = 'Лайки на ответы'

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Комментарий', related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Лайк на комментарий'
        verbose_name_plural = 'Лайки на комментарии'