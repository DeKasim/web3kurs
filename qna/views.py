from datetime import timedelta

from django.db.models import Q, Count
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from qna.models import Question, Answer, AnswerLike, Comment, CommentLike
from qna.serializers import QuestionSerializer, AnswerSerializer, CommentSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'question_text']
    filterset_fields = ['topic', 'author']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @method_decorator(cache_page(60 * 10))
    @action(detail=False, methods=['GET'])
    def dayly(self, request):
        """Вопросы за сегодня"""
        questions = Question.objects.filter(created_at__day=timezone.now().day)
        return Response(self.serializer_class(questions, many=True).data)

    @action(detail=False, methods=['GET'])
    def new_weekly(self, request):
        """Не мои вопросы за неделю или малым кол-вом ответов)"""
        date = timezone.now() - timedelta(days=7)
        questions = Question.objects.annotate(answer_count=Count('answers')).filter(
            (Q(created_at__gte=(date)) | Q(answer_count__lte=5)) & ~Q(author=request.user)).order_by('-answer_count')
        return Response(self.serializer_class(questions, many=True).data)

    @action(detail=False, methods=['GET'])
    def unanswered(self, request):
        """Вопросы без ответов"""
        questions = Question.objects.annotate(answer_count=Count('answers')).filter(answer_count=0)
        return Response(self.serializer_class(questions, many=True).data)

    @action(detail=False, methods=['GET'])
    def my(self, request):
        """Мои вопросы"""
        questions = Question.objects.filter(author=request.user)
        return Response(self.serializer_class(questions, many=True).data)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['answer_text']
    filterset_fields = ['question', 'author']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        answer = Answer.objects.get(pk=pk)
        like_obj = AnswerLike()
        like_obj.author = request.user
        like_obj.answer = answer
        like_obj.save()
        return Response(self.serializer_class(Answer.objects.get(pk=pk)).data)

    @action(detail=False, methods=['GET'])
    def my(self, request):
        """Мои ответы"""
        questions = Answer.objects.filter(author=request.user)
        return Response(self.serializer_class(questions, many=True).data)

    @action(detail=False, methods=['GET'])
    def my_top(self, request):
        """Мои ответы за неделю или большим кол-вом лайков"""
        date = timezone.now() - timedelta(days=7)
        questions = Question.objects.annotate(likes_count=Count('likes')).filter(
            (Q(created_at__gte=(date)) | ~Q(likes_count__lte=5)) & Q(author=request.user)).order_by('-likes_count')
        return Response(self.serializer_class(questions, many=True).data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['comment_text']
    filterset_fields = ['answer', 'author']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        like_obj = CommentLike()
        like_obj.author = request.user
        like_obj.comment = comment
        like_obj.save()
        return Response(self.serializer_class(Comment.objects.get(pk=pk)).data)
