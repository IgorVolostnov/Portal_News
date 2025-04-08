from django.contrib import admin
from .models import Author, Category, Post, Comment


class AuthorAdmin(admin.ModelAdmin):
    """The class for representing authors in the admin panel.

    Класс для представления авторов постов в панели администратора

    Атрибуты:
    ----------
    list_display -- кортеж с полями, представленными в таблице с авторами.
    """
    list_display = ('__str__', 'first_name', 'last_name', 'email', 'rating_user', 'last_login', 'date_joined')


class CategoryAdmin(admin.ModelAdmin):
    """The class for representing categories in the admin panel.

    Класс для представления категорий постов в панели администратора

    Атрибуты:
    ----------
    list_display -- кортеж с полями, представленными в таблице с авторами.
    """
    list_display = ('__str__', 'user_names')


class PostAdmin(admin.ModelAdmin):
    """The class for representing posts in the admin panel.

    Класс для представления постов в панели администратора

    Атрибуты:
    ----------
    list_display -- кортеж с полями, представленными в таблице с авторами.
    """
    list_display = ('post_title', 'post_text', 'post_author', 'post_type', 'post_categories', 'time_in_post', 'rating_post')


class CommentAdmin(admin.ModelAdmin):
    """The class for representing comments in the admin panel.

    Класс для представления комментариев к постам в панели администратора

    Атрибуты:
    ----------
    list_display -- кортеж с полями, представленными в таблице с авторами.
    """
    list_display = ('name_user', '__str__', 'name_post', 'time_in_comment', 'rating_comment')

# Регистрируем модели проекта в панели администратора
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)