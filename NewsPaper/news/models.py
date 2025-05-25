from django.conf.global_settings import MEDIA_URL
from django.db import models
from django.contrib.auth.models import User
from django.db.models import TextField, CharField
from django.urls import reverse
from django.core.cache import cache
from django.utils.safestring import mark_safe


class Author(models.Model):
    """The post authors model, linked one-to-one with the built-in User model.

        Модель авторов постов, связанная один к одному с встроенной моделью 'User'.

        Атрибуты:
        ----------
        user -- связь один к одному с встроенной моделью 'User'.

        rating_user -- целое число, отражающее совокупный рейтинг автора, рассчитанный в методе 'update_rating'.

        Методы:
        ----------
        __str__ -- строковое обозначение экземпляра модели, поле 'username' связанной встроенной модели 'User'.

        update_rating -- рассчитывает суммарный рейтинг автора, учитывая рейтинг постов автора,
        рейтинг оставленных комментариев под постами автора, а также рейтинги комментариев самого автора.
        """
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'авторы'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Автор')
    rating_user = models.IntegerField(default=0, verbose_name='Рейтинг автора')

    def __str__(self):
        return self.user.username

    def update_rating(self):
        total_rating_post = 0
        for _post in self.post_set.all():
            total_rating_post += (_post.rating_post * 3)
        total_rating_comment = 0
        for _comment in self.user.comment_set.all():
            total_rating_comment += _comment.rating_comment
        total_rating_comment_by_post_author = 0
        for _post in self.post_set.all():
            for _comment in _post.comment_set.all():
                total_rating_comment_by_post_author += _comment.rating_comment
        self.rating_user = total_rating_post + total_rating_comment + total_rating_comment_by_post_author
        self.save()


class Category(models.Model):
    """The post category model, which is linked many-to-many with the 'Post' model through an additional
        'PostCategory' model.

        Модель категорий постов, связанная многие ко многим с моделью 'Post' через дополнительную модель 'PostCategory'.

        Атрибуты:
        ----------
        name_category -- наименование категории.

        subscribers -- пользователи подписанные на категорию, связь many-to-many c встроенной моделью 'User'.

        Методы:
        ----------
        __str__ -- строковое обозначение экземпляра модели.

        get_absolute_url -- метод для генерации ссылок на категории с подробной информацией о постах по данной
        категории.
        """
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'
    new_news = 'NEW'
    popular = 'POP'
    internet = 'INT'
    sport = 'SPO'
    culture = 'CUL'
    politics = 'POL'
    society = 'SOC'
    technology = 'TEC'
    incidents = 'INC'
    economy = 'ECN'
    religion = 'REL'
    cars = 'CAR'
    show_business = 'SHB'
    wildlife = 'WIL'
    ecology = 'ECO'

    NEWS_CATEGORY = [
        (new_news, 'Свежее'),
        (popular, 'Популярное'),
        (incidents, 'Происшествия'),
        (sport, 'Спорт'),
        (show_business, 'Шоу-бизнес'),
        (internet, 'Интернет'),
        (cars, 'Автомобили'),
        (culture, 'Культура'),
        (politics, 'Политика'),
        (society, 'Общество'),
        (technology, 'Наука и технологии'),
        (economy, 'Экономика'),
        (religion, 'Религия'),
        (wildlife, 'Живая природа'),
        (ecology, 'Экология')
    ]
    name_category = models.CharField(max_length=3, choices=NEWS_CATEGORY, default=new_news, unique=True,
                                     verbose_name='Название категории')
    subscribers = models.ManyToManyField(User, through='SubscribersCategory')

    def __str__(self):
        dict_category = {
            'NEW': 'Свежее',
            'POP': 'Популярное',
            'INC': 'Происшествия',
            'SPO': 'Спорт',
            'SHB': 'Шоу-бизнес',
            'INT': 'Интернет',
            'CAR': 'Автомобили',
            'CUL': 'Культура',
            'POL': 'Политика',
            'SOC': 'Общество',
            'TEC': 'Наука и технологии',
            'ECN': 'Экономика',
            'REL': 'Религия',
            'WIL': 'Живая природа',
            'ECO': 'Экология',
        }
        return f'{dict_category[self.name_category]}'

    def get_absolute_url(self):
        return reverse(viewname='category_news_list', args=[str(self.id)])


class Post(models.Model):
    """The A post model that is one-to-many related to the 'Author' model
        and many-to-many related to the 'Category' model.

        Модель постов, связанная один ко многим с моделью 'Author' и многие ко многим с моделью 'Category'.

        Атрибуты:
        ----------
        title_post -- заголовок поста.

        text_post -- текст поста.

        author_post -- автор поста, связь one-to-many c моделью 'Author'.

        type_post -- вид поста: новость или статья.

        time_in_post -- время создания поста.

        rating_post -- целое число, которое отражает рейтинг поста. Изменяется методами 'like' и 'dislike'.

        category_post -- категория поста, связь many-to-many c моделью 'Category'.

        Методы:
        ----------
        __str__ -- строковое обозначение экземпляра модели.

        like -- увеличивает рейтинг поста на 1.

        dislike -- уменьшает рейтинг поста на 1.

        get_absolute_url -- метод для генерации ссылок на постам с подробной информацией.

        save -- метод удаления кэша при изменении экземпляра поста.

        preview -- метод обрезания текста до заданного количества символов.
        """
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'посты'

    news = 'NE'
    article = 'AR'
    KIND_CONTENT = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    title_post = models.CharField(max_length=255, verbose_name='Заголовок поста')
    text_post = models.TextField(blank=True, verbose_name='Текст поста')
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор поста')
    type_post = models.CharField(max_length=2, choices=KIND_CONTENT, verbose_name='Вид поста')
    time_in_post = models.DateTimeField(auto_now_add=True, verbose_name='Время поста')
    rating_post = models.IntegerField(default=0, verbose_name='Рейтинг поста')
    category_post = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория поста')


    def __str__(self):
        return f'{self.title_post.title()}: {self.preview(self.text_post)}'

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        if self.rating_post < 1:
            self.rating_post = 0
            self.save()
        else:
            self.rating_post -= 1
            self.save()

    def get_absolute_url(self):
        if self.type_post ==  'NE':
            return reverse('post_detail_news', args=[str(self.id)])
        else:
            return reverse('post_detail_articles', args=[str(self.id)])

    # Удаляем объект из кэша при изменении
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

    @staticmethod
    def preview(text: str | CharField | TextField):
        if len(text) < 40:
            preview_text = text
        else:
            preview_text = f'{text[:40]}...'
        return preview_text


class PostCategory(models.Model):
    """The model linking the 'Post' and 'Category' models.

        Модель связывающая модели 'Post' и 'Category'.

        Атрибуты:
        ----------
        post -- связь one-to-many c моделью 'Post'.

        category -- связь one-to-many c моделью 'Category'.

        Методы:
        ----------
        __str__ -- строковое обозначение экземпляра модели.
        """
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Перечень категорий'
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name='Наименование категории')

    def __str__(self):
        return f''


class PostImage(models.Model):
    """A post photo model linked one-to-many with the 'Post' model.

            Модель фотографий постов связанная один ко многим с моделью'Post'.

            Атрибуты:
            ----------
            post -- связь one-to-many c моделью 'Post'.

            images -- изображение модели 'Post'.

            Методы:
            ----------
            __str__ -- ссылка на изображение.
            """
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, related_name='photos',
                             verbose_name='Наименование поста')
    images = models.FileField(upload_to = 'images', verbose_name='Изображение')

    def __str__(self):
        return mark_safe(f"<img src='{MEDIA_URL + self.images.url}' width=200>")



class PostLinkImage(models.Model):
    """A model of links to photos of posts linked one-to-many with the 'Post' model.

            Модель ссылок на фотографии постов связанная один ко многим с моделью'Post'.

            Атрибуты:
            ----------
            post -- связь one-to-many c моделью 'Post'.

            links -- изображение модели 'Post'.

            Методы:
            ----------
            __str__ -- строковое обозначение экземпляра модели.
            """
    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, related_name='links',
                             verbose_name='Наименование поста')
    link = models.TextField(blank=True, verbose_name='Ссылка на изображение')

    def __str__(self):
        return self.link


class SubscribersCategory(models.Model):
    """The model linking the 'User' and 'Category' models.

        Модель связывающая модели 'User' и 'Category'.

        Атрибуты:
        ----------
        subscribers -- связь one-to-many c моделью 'User'.

        category -- связь one-to-many c моделью 'Category'.

        Методы:
        ----------
        __str__ -- строковое обозначение экземпляра модели.
        """
    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Имя Фамилия пользователя'
    subscribers = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Ник пользователя')
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.subscribers.first_name} {self.subscribers.last_name}'


class Comment(models.Model):
    """The A post model that is one-to-many related to the 'Author' model
            and many-to-many related to the 'Category' model.

        Модель комментариев, связанная один ко многим с моделью 'Post' и один ко многим с моделью 'User'.

            Атрибуты:
            ----------
            post_comment -- пост комментария, связь one-to-many c моделью 'Post'.

            user_comment -- пользователь комментария, связь one-to-many c моделью 'User'.

            text_comment -- текст комментария.

            time_in_comment -- время создания комментария.

            rating_comment -- целое число, которое отражает рейтинг комментария. Изменяется методами 'like' и 'dislike'.

            Методы:
            ----------
            __str__ -- строковое обозначение экземпляра модели.

            like -- увеличивает рейтинг комментария на 1.

            dislike -- уменьшает рейтинг комментария на 1.

            preview -- метод обрезания текста до заданного количества символов.
            """
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'комментарии'

    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост комментария')
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь комментария')
    text_comment = models.TextField(blank=True, verbose_name='Текст комментария')
    time_in_comment = models.DateTimeField(auto_now_add = True, verbose_name='Дата и время комментария')
    rating_comment = models.IntegerField(default=0, verbose_name='Рейтинг комментария')

    def __str__(self):
        return self.preview(self.text_comment)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        if self.rating_comment < 1:
            self.rating_comment = 0
            self.save()
        else:
            self.rating_comment -= 1
            self.save()

    @staticmethod
    def preview(text: str | TextField):
        if len(text) < 40:
            preview_text = text
        else:
            preview_text = f'{text[:40]}...'
        return preview_text