# backend/app/tasks/seedbox_tasks.py
from app.celery_worker import celery
from app.core.database import SessionLocal
from app.models.seedbox import SeedBox
from app.models.smtp_account import SMTPAccount
from app.utils.email_sender import send_email
from app.core.config import settings
from datetime import datetime
import random
import logging

logger = logging.getLogger(__name__)

@celery.task(bind=True)
def send_seed_test_task(self, seedbox_id: int, user_id: int):
    """
    Celery task to send a test email to a seedbox and simulate inbox/spam result.
    """
    db = SessionLocal()
    try:
        seedbox = db.query(SeedBox).filter(
            SeedBox.id == seedbox_id,
            SeedBox.user_id == user_id
        ).first()

        if not seedbox:
            logger.error("Seedbox not found (id=%s user=%s)", seedbox_id, user_id)
            return {"status": "error", "detail": "Seedbox not found"}

        smtp = db.query(SMTPAccount).filter(
            SMTPAccount.user_id == user_id,
            SMTPAccount.is_active == True
        ).first()

        if not smtp:
            logger.error("No active SMTP account for user %s", user_id)
            return {"status": "error", "detail": "No SMTP account available"}

        subject = f"[Async Seed Test] Inbox check - {datetime.utcnow().isoformat()}"
        body = f"This is a seed inbox placement test sent to {seedbox.email_address}."

        send_email(
            smtp_config={
                "host": smtp.host,
                "port": smtp.port,
                "username": smtp.username,
                "password": smtp.password,
                "use_tls": smtp.port == 587,
            },
            to_address=seedbox.email_address,
            subject=subject,
            body=body,
            from_name=settings.FROM_NAME,
            from_email=settings.FROM_EMAIL,
            reply_to=settings.REPLY_TO,
        )

        result = random.choice(["inbox", "spam"])
        seedbox.last_status = result
        seedbox.last_checked = datetime.utcnow()
        db.add(seedbox)
        db.commit()

        logger.info("✅ Async seed test complete: %s → %s", seedbox.email_address, result)
        return {"status": "success", "seedbox_id": seedbox_id, "result": result}

    except Exception as e:
        logger.exception("❌ Failed async seed test")
        return {"status": "error", "detail": str(e)}
    finally:
        db.close()
