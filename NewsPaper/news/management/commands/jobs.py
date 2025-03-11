import logging
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django_apscheduler.models import DjangoJobExecution
from ..list_post import Generator

logger = logging.getLogger(__name__)


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

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)