from django.db import models
from django.contrib.auth.models import User
from django.db.models import TextField, CharField
from django.urls import reverse
from django.core.cache import cache


# Модель категорий постов, связанная многие ко многим с моделью Post через дополнительную модель PostCategory и
# связанная многие ко многим с встроенной моделью User через дополнительную модель SubscribersCategory
class Category(models.Model):
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
    name_category = models.CharField(max_length=3, choices=NEWS_CATEGORY, default=new_news,
                                     unique=True)
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

    def user_names(self):
        return u" %s" % (u", ".join([author.username for author in self.subscribers.all()]))

    user_names.short_description = u'Подписчики'

    def get_absolute_url(self):
        return reverse('category_news_list', args=[str(self.id)])


# Модель авторов постов, связанная один к одному с встроенной моделью User
class Author(models.Model):
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'авторы'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rating_user = models.IntegerField(default=0)
    rating_user.verbose_name = 'Рейтинг автора'

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

    def __str__(self):
        return self.user.username

    def first_name(self):
        return self.user.first_name

    first_name.short_description = u'Имя'

    def last_name(self):
        return self.user.last_name

    last_name.short_description = u'Фамилия'

    def email(self):
        return self.user.email

    email.short_description = u'Электронная почта'

    def last_login(self):
        return self.user.last_login

    last_login.short_description = u'Последний визит'

    def date_joined(self):
        return self.user.date_joined

    date_joined.short_description = u'Дата регистрации'


# Модель постов, связанная многие ко многим с моделью Category через дополнительную модель PostCategory и
# связанная один к одному с моделью Author
class Post(models.Model):
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'посты'

    news = 'NE'
    article = 'AR'
    KIND_CONTENT = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=2, choices=KIND_CONTENT)
    time_in_post = models.DateTimeField(auto_now_add=True)
    category_post = models.ManyToManyField(Category, through='PostCategory')
    title_post = models.CharField(max_length=255)
    text_post = models.TextField(blank=True)
    rating_post = models.IntegerField(default=0)

    time_in_post.verbose_name = 'Время поста'
    rating_post.verbose_name = 'Рейтинг поста'

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

    def __str__(self):
        return f'{self.title_post.title()}: {self.preview(self.text_post)}'

    def post_title(self):
        return self.preview(self.title_post)

    post_title.short_description = u'Заголовок поста'

    def post_text(self):
        return self.preview(self.text_post)

    post_text.short_description = u'Текст поста'

    def post_author(self):
        return self.author_post.user.username

    post_author.short_description = u'Автор поста'

    def post_type(self):
        dict_types = {
            'NE': 'Новость',
            'AR': 'Статья'
        }
        return f'{dict_types[self.type_post]}'

    post_type.short_description = u'Вид поста'

    def post_categories(self):
        return u" %s" % (u", ".join([category.__str__() for category in self.category_post.all()]))

    post_categories.short_description = u'Категории поста'

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


# Модель связывающая модели Post и Category
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


# Модель связывающая модели User и Category
class SubscribersCategory(models.Model):
    subscribers = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


# Модель комментариев, связанная один к одному с моделью Post и связанная один к одному с моделью User
class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'комментарии'

    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField(blank=True)
    time_in_comment = models.DateTimeField(auto_now_add = True)
    rating_comment = models.IntegerField(default=0)

    time_in_comment.verbose_name = 'Время комментария'
    rating_comment.verbose_name = 'Рейтинг комментария'

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

    def __str__(self):
        return self.preview(self.text_comment)

    def name_post(self):
        return self.preview(self.post_comment.title_post)

    name_post.short_description = u'Название поста'

    def name_user(self):
        return self.user_comment.username

    name_user.short_description = u'Имя пользователя'

    @staticmethod
    def preview(text: str | TextField):
        if len(text) < 40:
            preview_text = text
        else:
            preview_text = f'{text[:40]}...'
        return preview_text