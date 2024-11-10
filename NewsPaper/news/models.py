from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rating_user = models.IntegerField(default=0)

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

