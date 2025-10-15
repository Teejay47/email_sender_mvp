# backend/app/tasks/reset_counters.py
from datetime import datetime
import logging
from app.core.database import SessionLocal
from app.models.smtp_account import SMTPAccount
from app.celery_worker import celery

logger = logging.getLogger(__name__)

def _do_reset_hourly():
    """Reset the hourly_sent counter for all SMTP accounts."""
    try:
        with SessionLocal() as db:
            updated = db.query(SMTPAccount).update({SMTPAccount.hourly_sent: 0})
            db.commit()
        logger.info(
            "reset_smtp_counters: reset hourly_sent for %d SMTP accounts at %s",
            updated,
            datetime.utcnow().isoformat()
        )
    except Exception:
        logger.exception("reset_smtp_counters failed")

def _do_reset_daily():
    """Reset the used_today counter for all SMTP accounts."""
    try:
        with SessionLocal() as db:
            updated = db.query(SMTPAccount).update({SMTPAccount.used_today: 0})
            db.commit()
        logger.info(
            "reset_daily_used_today: reset used_today for %d SMTP accounts at %s",
            updated,
            datetime.utcnow().isoformat()
        )
    except Exception:
        logger.exception("reset_daily_used_today failed")

@celery.task(name='app.tasks.reset_counters.reset_smtp_counters', bind=True)
def reset_smtp_counters(self):
    """Celery task wrapper to reset hourly_sent counters."""
    logger.info("Task %s: Starting reset_smtp_counters", self.request.id)
    _do_reset_hourly()
    logger.info("Task %s: Completed reset_smtp_counters", self.request.id)
    return {"status": "ok"}

@celery.task(name='app.tasks.reset_counters.reset_daily_used_today', bind=True)
def reset_daily_used_today(self):

    """Celery task wrapper to reset daily used_today counters."""
    logger.info("Task %s: Starting reset_daily_used_today", self.request.id)
    _do_reset_daily()
    logger.info("Task %s: Completed reset_daily_used_today", self.request.id)
    return {"status": "ok"}
