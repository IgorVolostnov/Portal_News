import os
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_mails_every_subscribers': {
        'task': 'news.tasks.send_mail_job',
        'schedule': crontab(hour='08', minute='00', day_of_week='monday'),
    },
}