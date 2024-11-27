from datetime import timedelta

from django.core.mail import send_mail
from django.utils import timezone

from djangoQnA.celery import app
from django.contrib.auth.models import User

from qna.models import Question, Topic


@app.task
def mailing_new_question():
    date = timezone.now() - timedelta(days=7)
    users_email = [user.email for user in User.objects.all()]
    message = "Новые вопросы этой недели\n\n"
    questions = Question.objects.filter(created_at__gte=date)
    for i, question in enumerate(questions, start=1):
        message += f"{i}. {question.title}\n"
    send_mail('Вопросы этой недели', message, 'noreply@site.ru', users_email)


@app.task
def weekly_survey():
    question = Question()
    question.author = User.objects.get(username='admin')
    question.title = 'Как прошла неделя?'
    question.question_text = 'Сколько вопросов задали? На сколько ответили? И как в целом прошла ваша неделя?'
    question.topic = Topic.objects.get(pk=1)
    question.save()
