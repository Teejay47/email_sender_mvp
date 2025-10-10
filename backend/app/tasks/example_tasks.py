from .celery import celery


# Note: If you name this file example_tasks.py, Celery autodiscover should find tasks
from app.celery_worker import celery


@celery.task(name="tasks.add")
def add(x, y):
    return x + y