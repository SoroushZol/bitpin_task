import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitpin_task.settings')

app = Celery('bitpin_task')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
