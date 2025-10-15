"""Shim re-exporting celery instance from celery_worker.py"""
try:
    from .celery_worker import celery
except Exception:
    from celery import Celery
    from app.core.config import settings
    celery = Celery("app", broker=getattr(settings, "CELERY_BROKER_URL", "redis://redis:6379/0"))
