from celery import Celery
from app.core.config import settings

celery = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Explicitly import tasks so Celery registers them
import app.tasks.seedbox_tasks
import app.tasks.recipient_tasks
# add more imports as needed

celery.autodiscover_tasks(["app.tasks"])
