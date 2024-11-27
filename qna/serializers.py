from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from qna.models import Question, Answer, Topic, Comment, User


ban_words = ['хуй', 'пизда']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class QuestionSerializer(serializers.ModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())
    author = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'topic', 'question_text', 'created_at', 'updated_at', 'author',)
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        if len(attrs['question_text']) < 5:
            raise ValidationError({'question_text': 'Вопрос должен быть больше 5 символов'})
        for ban_word in ban_words:
            if ban_word in attrs['question_text'].lower():
                raise ValidationError({'question_text': 'Вопрос не должен содержать нецензурную лексику'})
            if ban_word in attrs['title'].lower():
                raise ValidationError({'title': 'Заголовок не должен содержать нецензурную лексику'})
        return attrs


class AnswerSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'author', 'question', 'answer_text', 'created_at', 'updated_at', 'likes_count')
        read_only_fields = ['id', 'created_at', 'updated_at', 'likes_count']
        # depth = 1

    def validate(self, attrs):
        if len(attrs['answer_text']) < 5:
            raise ValidationError({'answer_text': 'Ответ должен быть больше 5 символов'})
        for ban_word in ban_words:
            if ban_word in attrs['answer_text'].lower():
                raise ValidationError({'answer_text': 'Ответ не должен содержать нецензурную лексику'})


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class CommentLikeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AnswerLikeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
