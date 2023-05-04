import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsprj.settings')

app = Celery('newsprj')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'newsapp.tasks.every_wk_news_mailing',
        'schedule': 30.0,
        # 'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # 'args': (agrs),
    },
}

app.autodiscover_tasks()

