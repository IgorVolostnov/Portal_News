# Generated by Django 5.1.3 on 2024-11-10 18:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_post', models.CharField(choices=[('NE', 'Новость'), ('AR', 'Статья')], max_length=2)),
                ('time_in_post', models.DateTimeField(auto_now_add=True)),
                ('title_post', models.CharField(max_length=255)),
                ('text_post', models.TextField(blank=True)),
                ('rating_post', models.IntegerField(default=0)),
                ('author_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_comment', models.TextField(blank=True)),
                ('time_in_comment', models.DateTimeField(auto_now_add=True)),
                ('rating_comment', models.IntegerField(default=0)),
                ('user_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='category_post',
            field=models.ManyToManyField(through='news.PostCategory', to='news.category'),
        ),
    ]