import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'games.settings')

app = Celery('games')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_url = 'redis://default:@localhost:6379/0'

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'yo yo Request: {self.request!r}')