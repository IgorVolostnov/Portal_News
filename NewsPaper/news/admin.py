from dataclasses import fields

from django.conf.global_settings import MEDIA_URL
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Author, Post, Comment, Category, PostImage, PostLinkImage


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """The class for representing authors in the admin panel.

    Класс для представления авторов постов в панели администратора.

    Атрибуты:
    ----------
    list_display -- кортеж с полями, представленными в таблице с авторами.

    search_fields -- кортеж с полями, в которых будет происходит поиск, введенного текста в поисковой строке.

    list_per_page -- количество экземпляров объекта на одной странице.

    Методы:
    ----------
    name_user -- имя автора, поле 'first_name' связанной встроенной модели 'User'.

    surname_user -- фамилия автора, поле 'last_name' связанной встроенной модели 'User'.

    email_user -- электронная почта автора, поле 'email' связанной встроенной модели 'User'.

    last_login_user -- последняя авторизация автора на сайте, поле 'last_login' связанной встроенной модели 'User'.

    date_joined_user -- дата регистрации автора на сайте, поле 'date_joined' связанной встроенной модели 'User'.

    get_ordering -- сортировка по умолчанию.
    """
    list_display = ('__str__', 'name_user', 'surname_user', 'email_user', 'rating_user', 'last_login_user',
                    'date_joined_user')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'user__last_login',
                     'user__date_joined')
    list_per_page = 20

    @admin.display(description='Имя')
    def name_user(self, obj):
        return obj.user.first_name

    name_user.admin_order_field = 'user__first_name'

    @admin.display(description='Фамилия')
    def surname_user(self, obj):
        return obj.user.last_name

    surname_user.admin_order_field = 'user__last_name'

    @admin.display(description='Электронная почта')
    def email_user(self, obj):
        return obj.user.email

    email_user.admin_order_field = 'user__email'

    @admin.display(description='Последний визит')
    def last_login_user(self, obj):
        return obj.user.last_login

    last_login_user.admin_order_field = 'user__last_login'

    @admin.display(description='Дата регистрации')
    def date_joined_user(self, obj):
        return obj.user.date_joined

    date_joined_user.admin_order_field = 'user__date_joined'

    def get_ordering(self, request):
        return ('user__username',)


class SubscribersCategoryInline(admin.TabularInline):
    """The class for representing the 'Subscribers Category' model, a manu-to-many relationship
    between the 'Category' and 'User' models.

    Класс для представления модели 'SubscribersCategory', связь manu-to-many между моделями 'Category' и 'User'.

    Атрибуты:
    ----------
    model -- связь many-to-many с моделью 'User' через атрибут 'subscribers'.
    """
    model = Category.subscribers.through


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """The class for representing post categories in the admin panel.

    Класс для представления категорий постов в панели администратора.

    Атрибуты:
    ----------
    list_display -- кортеж с полями, представленными в таблице с категориями.

    inlines -- кортеж с полями для отображения пользователей, которые подписаны на экземпляр модели 'Category'.

    list_filter -- кортеж с полями, по которым необходимо отобразить фильтры в таблице с категориями.

    list_per_page -- количество экземпляров объекта на одной странице.

    Методы:
    ----------
    id_category -- id-номер категории.

    name_category -- наименование категории'.

    get_ordering -- сортировка по умолчанию.
    """
    list_display = ('name_category', 'id_category')
    inlines = (SubscribersCategoryInline,)
    list_filter = ('subscribers',)
    list_per_page = 20

    @admin.display(description='№')
    def id_category(self, obj):
        return obj.pk

    id_category.admin_order_field = 'pk'

    @admin.display(description='№')
    def name_category(self, obj):
        return obj.name_category

    name_category.admin_order_field = 'name_category'

    def get_ordering(self, request):
        return ('pk',)


class PostCategoryInline(admin.TabularInline):
    """The class for representing the 'PostCategory' model, a many-to-many relationship
    between the 'Post' and 'Category' models.

    Класс для представления модели 'PostCategory', связь manu-to-many между моделями 'Post' и 'Category'.

    Атрибуты:
    ----------
    model -- связь many-to-many с моделью 'Category' через атрибут 'category_post'.
    """
    model = Post.category_post.through


class PostImageInline(admin.StackedInline):
    """The class for representing the 'PostImage' model, a one-to-many relationship
    between the 'Post' and 'Image' models.

    Класс для представления модели 'PostImage', связь one-to-many между моделями 'Post' и 'PostImage'.

    Атрибуты:
    ----------
    model -- связь one-to-many между моделями 'Post' и 'PostImage'.
    """
    model = PostImage


class PostLinkImageAdmin(admin.StackedInline):
    """The class for representing the 'PostLinkImage' model, a one-to-many relationship
    between the 'Post' and 'PostLinkImage' models.

    Класс для представления модели 'PostLinkImage', связь one-to-many между моделями 'Post' и 'PostLinkImage'.

    Атрибуты:
    ----------
    model -- связь one-to-many между моделями 'Post' и 'PostLinkImage'.
    """
    model = PostLinkImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """The class for presenting posts in the admin panel.

        Класс для представления постов в панели администратора.

        Атрибуты:
        ----------
        list_display -- кортеж с полями, представленными в таблице с постами.

        inlines -- кортеж с полями для отображения категорий, к которым относится данный пост.

        list_filter -- кортеж с полями, по которым необходимо отобразить фильтры в таблице с постами.

        search_fields -- кортеж с полями, в которых будет происходит поиск, введенного текста в поисковой строке.

        list_per_page -- количество экземпляров объекта на одной странице.

        Методы:
        ----------
        post_title -- заголовок поста, поле 'title_post' модели 'Post'.

        post_text -- текст поста, поле 'text_post' модели 'Post'.

        post_author -- автор поста, поле 'username' связанной встроенной модели 'User'.

        post_type -- вид поста, поле 'type_post' модели 'Post'.

        time_post -- дата и время создания поста, поле 'time_in_post' модели 'Post'.

        value_rating_post -- рейтинг поста, поле 'rating_post' модели 'Post'.

        id_post -- id-номер поста, поле 'pk' модели 'Post'.

        get_ordering -- сортировка по умолчанию.
        """
    list_display = ('post_title', 'post_text', 'post_author', 'post_type', 'time_post', 'value_rating_post', 'id_post')
    inlines = (PostCategoryInline, PostImageInline, PostLinkImageAdmin)
    list_filter = ('category_post', 'type_post')
    search_fields = ('title_post', 'text_post', 'author_post__user__username', 'type_post', 'time_in_post',
                     'rating_post')
    list_per_page = 20

    @admin.display(description='Заголовок поста')
    def post_title(self, obj):
        return obj.preview(obj.title_post)

    post_title.admin_order_field = 'title_post'

    @admin.display(description='Текст поста')
    def post_text(self, obj):
        return obj.preview(obj.text_post)

    post_text.admin_order_field = 'text_post'

    @admin.display(description='Автор поста')
    def post_author(self, obj):
        return obj.author_post.user.username

    post_author.admin_order_field = 'author_post__user__username'

    @admin.display(description='Вид поста')
    def post_type(self, obj):
        dict_types = {
            'NE': 'Новость',
            'AR': 'Статья'
        }
        return f'{dict_types[obj.type_post]}'

    post_type.admin_order_field = 'type_post'

    @admin.display(description='Дата и время поста')
    def time_post(self, obj):
        return obj.time_in_post

    time_post.admin_order_field = 'time_in_post'

    @admin.display(description='Рейтинг поста')
    def value_rating_post(self, obj):
        return obj.rating_post

    value_rating_post.admin_order_field = 'rating_post'

    @admin.display(description='№')
    def id_post(self, obj):
        return obj.pk

    id_post.admin_order_field = 'pk'

    def get_ordering(self, request):
        return ('pk',)


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'post_photo')

    @admin.display(description='Наименование поста')
    def post_photo(self, obj):
        return obj.post.title_post

@admin.register(PostLinkImage)
class PostLinkImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """The class for submitting comments to posts in the admin panel.

        Класс для представления комментариев к постам в панели администратора.

        Атрибуты:
        ----------
        list_display -- кортеж с полями, представленными в таблице с комментариями.

        list_filter -- кортеж с полями, по которым необходимо отобразить фильтры в таблице с комментариями.

        search_fields -- кортеж с полями, в которых будет происходит поиск, введенного текста в поисковой строке.

        list_per_page -- количество экземпляров объекта на одной странице.

        Методы:
        ----------
        name_user -- пользователь комментария, поле 'username' связанной встроенной модели 'User'.

        name_post -- заголовок поста, поле 'title_post' модели 'Post'.

        time_in_comment -- дата и время создания комментария, поле 'time_in_comment' модели 'Comment'.

        rating_comment -- рейтинг комментария, поле 'rating_comment' модели 'Comment'.

        id_comment -- id-номер комментария, поле 'pk' модели 'Comment'.

        get_ordering -- сортировка по умолчанию.
        """
    list_display = ('__str__', 'name_user', 'name_post', 'time_in_comment', 'rating_comment', 'id_comment')
    list_filter = ('user_comment',)
    search_fields = ('user_comment__username', 'post_comment__title_post', 'time_in_comment', 'rating_comment')
    list_per_page = 20

    @admin.display(description='Пользователь комментария')
    def name_user(self, obj):
        return obj.user_comment.username

    name_user.admin_order_field = 'user_comment__username'

    @admin.display(description='Название поста')
    def name_post(self, obj):
        return obj.preview(obj.post_comment.title_post)

    name_post.admin_order_field = 'post_comment__title_post'

    @admin.display(description='Дата и время комментария')
    def time_in_comment(self, obj):
        return obj.time_in_comment

    time_in_comment.admin_order_field = 'time_in_comment'

    @admin.display(description='Рейтинг комментария')
    def rating_comment(self, obj):
        return obj.rating_comment

    rating_comment.admin_order_field = 'rating_comment'

    @admin.display(description='№')
    def id_comment(self, obj):
        return obj.pk

    id_comment.admin_order_field = 'pk'

    def get_ordering(self, request):
        return ('pk',)