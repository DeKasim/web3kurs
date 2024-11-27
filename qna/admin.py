from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from import_export.widgets import ForeignKeyWidget

from .models import Question, Answer, Topic, User, Comment, CommentLike, AnswerLike


class QuestionResource(resources.ModelResource):
    author_email = fields.Field(
        column_name='Author Email',
        attribute='author',
        widget=ForeignKeyWidget(User, 'email')
    )

    class Meta:
        model = Question
        fields = ('id', 'title', 'author_email', 'topic', 'question_text', 'created_at', 'updated_at')

    def dehydrate_title(self, question):
        return f"{question.title} (Exported)"

    def get_author_email(self, question):
        return question.author.email if question.author.email else "н/д"


class AnswerResource(resources.ModelResource):
    class Meta:
        model = Answer


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin, ExportActionMixin):
    list_display = ('title', 'author', 'question_text', 'created_at', )
    list_filter = ('created_at', 'author')
    date_hierarchy = 'created_at'
    search_fields = ('title', 'question_text')
    fields = ('title', ('author', 'topic'), 'question_text', ('created_at', 'updated_at'),)
    readonly_fields = ('created_at', 'updated_at', )

    resource_class = QuestionResource

    def get_export_queryset(self, request):
        return super().get_export_queryset(request).filter(created_at__year__gte=2000)


@admin.register(Answer)
class AnswerAdmin(ImportExportModelAdmin, ExportActionMixin):
    list_display = ('question', 'author', 'answer_text', 'created_at', 'likes_count')
    list_filter = ('created_at', 'author')
    date_hierarchy = 'created_at'
    search_fields = ('answer_text', )
    fields = ('question', 'author', 'answer_text', ('created_at', 'updated_at'), 'likes_count')
    readonly_fields = ('created_at', 'updated_at', 'likes_count')
    resource_classes = AnswerResource


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment_text')


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment')


@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'answer')
