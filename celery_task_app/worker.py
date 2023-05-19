import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_BACKEND_URL = os.getenv('CELERY_BACKEND_URL')

app = Celery(
    'celery_app',
    broker=CELERY_BROKER_URL,
    backend=CELERY_BACKEND_URL,
    include=['celery_task_app.tasks']
)
