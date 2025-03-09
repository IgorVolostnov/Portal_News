from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Author


# При создании экземпляра User, создаем экземпляр Author
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# При создании нового поста (новости или статьи), отправляем подписчикам на категорию письма
@receiver(m2m_changed, sender=Post.category_post.through)
def mail_to_subscribers(sender, instance, action, **kwargs):
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
    if action == 'post_add':
        # Получаем множество со всеми категориями и id-пользователей, подписанными на эти категории
        subscribers = set(instance.category_post.values_list('name_category', 'subscribers').all())
        print(Site.objects.get_current())
        if '127.0.0.1' in str(Site.objects.get_current()):
            url_post = f'http://127.0.0.1:8000{instance.get_absolute_url()}'
        else:
            url_post = f'{Site.objects.get_current()}{instance.get_absolute_url()}'
        # Для рассылки формируем словарь с подписчиками
        dict_subscribers = {}
        for subscriber in subscribers:
            if subscriber[1] is not None:
                current_user = User.objects.get(pk=subscriber[1])
                try:
                    dict_subscribers[dict_category[subscriber[0]]][current_user.email] = current_user.username
                except KeyError:
                    dict_subscribers[dict_category[subscriber[0]]] = {current_user.email: current_user.username}
        # Отправляем письма всем подписчикам по всем категориям, указанным в новости или статье
        for item in dict_subscribers.values():
            for email_user, username_user in item.items():
                # Получаем наш html-макет
                html_content = render_to_string(
                    'category_mail.html',
                    {
                        'user_name': username_user,
                        'text_title': instance.title_post,
                        'text_content': instance.text_post,
                        'url_content': url_post,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f'Здравствуй, {username_user}. Новая статья в твоём любимом разделе!',
                    body=instance.text_post,
                    to=[email_user],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
