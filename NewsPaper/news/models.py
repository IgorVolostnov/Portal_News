from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rating_user = models.IntegerField(default=0)

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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Category(models.Model):
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
        return reverse('category_news_list', args=[str(self.id)])


class Post(models.Model):
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

    def preview(self):
        if len(self.text_post) < 40:
            preview_text = self.text_post
        else:
            preview_text = f'{self.text_post[:40]}...'
        return preview_text

    def __str__(self):
        return f'{self.title_post.title()}: {self.preview()}'

    def get_absolute_url(self):
        if self.type_post ==  'NE':
            return reverse('post_detail_news', args=[str(self.id)])
        else:
            return reverse('post_detail_articles', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField(blank=True)
    time_in_comment = models.DateTimeField(auto_now_add = True)
    rating_comment = models.IntegerField(default=0)

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
