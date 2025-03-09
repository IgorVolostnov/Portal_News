# Generated by Django 5.1.5 on 2025-03-07 19:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_subscriberscategory'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(through='news.SubscribersCategory', to=settings.AUTH_USER_MODEL),
        ),
    ]
