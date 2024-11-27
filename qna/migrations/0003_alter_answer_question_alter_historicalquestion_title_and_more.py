# Generated by Django 5.1.4 on 2024-12-13 08:21

import django.core.validators
import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0002_historicalanswer_historicalquestion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='qna.question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='historicalquestion',
            name='title',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('[0-9a-zA-Za-яA-Я ?,.-]', 'В названии вопроса допустимы буквы, цифры, пробелы, и знаки препинания')], verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('[0-9a-zA-Za-яA-Я ?,.-]', 'В названии вопроса допустимы буквы, цифры, пробелы, и знаки препинания')], verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('[0-9a-zA-Za-яA-Я -]', 'В названии темы допустимы только буквы и цифры')]),
        ),
        migrations.CreateModel(
            name='AnswerLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qna.answer', verbose_name='Ответ')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=200, verbose_name='Содержимое')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qna.answer', verbose_name='Ответ')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ответ')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qna.comment', verbose_name='Комментарий')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalComment',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=200, verbose_name='Содержимое')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Время изменения')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('answer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='qna.answer', verbose_name='Ответ')),
                ('author', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical comment',
                'verbose_name_plural': 'historical comments',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
