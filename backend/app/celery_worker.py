# backend/app/celery_worker.py
import logging
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# ⚙️ Celery Initialization
# ---------------------------------------------------------------------
celery = Celery(
    "email_sender_mvp",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# ---------------------------------------------------------------------
# 🔧 Celery Configuration
# ---------------------------------------------------------------------
celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    worker_concurrency=4,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
    task_time_limit=600,
    result_expires=3600,
)

# ---------------------------------------------------------------------
# 🔍 Auto-discover tasks
# ---------------------------------------------------------------------
# This automatically finds all tasks in app/tasks/*
# so you don't need to manually list them in "include"
celery.autodiscover_tasks(["app"])

# ---------------------------------------------------------------------
# 🕒 Celery Beat Schedule
# ---------------------------------------------------------------------
celery.conf.beat_schedule = {
    "reset-hourly-smtp-counters": {
        "task": "app.tasks.reset_counters.reset_smtp_counters",
        "schedule": crontab(minute=5),
        "options": {"queue": "maintenance"},
    },
    "reset-daily-used_today": {
        "task": "app.tasks.reset_counters.reset_daily_used_today",
        "schedule": crontab(hour=0, minute=10),
        "options": {"queue": "maintenance"},
    },
}

# ---------------------------------------------------------------------
# 🚀 Logging
# ---------------------------------------------------------------------
logger.info("✅ Celery worker initialized")
logger.info("Broker: %s", settings.CELERY_BROKER_URL)
logger.info("Backend: %s", settings.CELERY_RESULT_BACKEND)
