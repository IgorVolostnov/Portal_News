from celery import shared_task
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
# from .management.list_post import Generator


# При создании нового поста (новости или статьи), отправляем подписчикам на категорию письма
@shared_task
def mail_to_subscribers(oid):
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
    # Получаем множество со всеми категориями и id-пользователей, подписанными на эти категории
    current_post = Post.objects.get(pk=oid)
    subscribers = set(current_post.category_post.values_list('name_category', 'subscribers').all())
    print(Site.objects.get_current())
    if '127.0.0.1' in str(Site.objects.get_current()):
        url_post = f'http://127.0.0.1:8000{current_post.get_absolute_url()}'
    else:
        url_post = f'{Site.objects.get_current()}{current_post.get_absolute_url()}'
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
                    'text_title': current_post.title_post,
                    'text_content': current_post.text_post,
                    'url_content': url_post,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {username_user}. Новая статья в твоём любимом разделе!',
                body=current_post.text_post,
                to=[email_user],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

@shared_task
def send_mail_job():
    generator_data = Generator()
    data_post_last_week = generator_data.get_query()
    for subscriber in data_post_last_week:
        title_post = (f'Здравствуйте, {subscriber['username_user']}. '
                      f'Новые новости и статьи за прошедшую неделю по Вашим любимым категориям!')
        html_content = render_to_string(
            template_name='send_mail_posts_week.html',
            context={
                'text_title': title_post,
                'categories': subscriber['categories'],
            }
        )
        msg = EmailMultiAlternatives(
            subject=title_post,
            body=title_post,
            to=[subscriber['email_user']],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()