from django.contrib import admin
from django.urls import include, path
from rest_framework import routers, permissions


from qna import views

router = routers.DefaultRouter()
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'comments', views.CommentViewSet)

from rest_framework.schemas import get_schema_view
from rest_framework.schemas.openapi import SchemaGenerator

schema_view = get_schema_view(
    title="Документация",
    description="Вопросы и ответы по разным категориям с оценками",
    version="1.0.0",
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=SchemaGenerator,
)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
