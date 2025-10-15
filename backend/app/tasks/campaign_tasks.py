# backend/app/tasks/campaign_tasks.py
from datetime import datetime
import time
import logging

from celery import shared_task
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from app.core.database import SessionLocal
from app.core.security import fernet
from app.models.campaign_batch import CampaignBatch
from app.models.campaign import Campaign
from app.models.smtp_account import SMTPAccount
from app.models.recipient import Recipient
from app.models.email_log import EmailLog
from app.utils.email_sender import send_email

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


def get_db_session() -> Session:
    """Helper to create a fresh database session for Celery workers."""
    return SessionLocal()



@shared_task(bind=True, max_retries=MAX_RETRIES, default_retry_delay=60)
def send_batch(self, batch_id: int):
    db = get_db_session()
    try:
        batch: CampaignBatch = (
            db.query(CampaignBatch)
            .filter(CampaignBatch.id == batch_id)
            .first()
        )
        if not batch:
            logger.warning("send_batch: batch %s not found", batch_id)
            return {"status": "error", "message": "Batch not found"}

        campaign: Campaign = (
            db.query(Campaign)
            .filter(Campaign.id == batch.campaign_id)
            .first()
        )

        # Lock SMTP row to avoid concurrent counter corruption
        try:
            smtp_acc: SMTPAccount = (
                db.query(SMTPAccount)
                .filter(SMTPAccount.id == batch.smtp_account_id)
                .with_for_update()
                .first()
            )
        except OperationalError as e:
            logger.warning(
                "Database lock contention on SMTP %s, retrying...",
                batch.smtp_account_id,
            )
            raise self.retry(exc=e, countdown=5)

        if not campaign or not smtp_acc:
            batch.paused = True
            db.add(batch)
            db.commit()
            logger.warning(
                "send_batch: missing campaign or smtp for batch %s", batch_id
            )
            return {"status": "error", "message": "Missing campaign or SMTP account"}

        if batch.paused:
            return {"status": "skipped", "message": "Batch is paused"}

        # --- Step 1: Auto-create EmailLogs if missing ---
        recipients = (
            db.query(Recipient)
            .filter(Recipient.validated == True, Recipient.suppressed == False)
            .all()
        )

        for r in recipients:
            exists = (
                db.query(EmailLog)
                .filter(
                    EmailLog.campaign_id == campaign.id,
                    EmailLog.batch_id == batch.id,
                    EmailLog.recipient_id == r.id,
                )
                .first()
            )
            if not exists:
                log = EmailLog(
                    campaign_id=campaign.id,
                    recipient_id=r.id,
                    batch_id=batch.id,
                    smtp_account_id=smtp_acc.id,
                    status="pending",
                    attempts=0,
                    timestamp=datetime.utcnow(),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                db.add(log)
        db.commit()

        # --- Step 2: Fetch pending logs ---
        pending_logs = (
            db.query(EmailLog)
            .filter(EmailLog.batch_id == batch.id, EmailLog.status == "pending")
            .all()
        )

        if not pending_logs:
            batch.completed_at = datetime.utcnow()
            db.add(batch)
            db.commit()
            return {"status": "completed", "message": "No recipients to send"}

        # --- Step 3: Prepare SMTP config ---
        smtp_password = None
        try:
            if smtp_acc.encrypted_password:
                smtp_password = (
                    fernet.decrypt(smtp_acc.encrypted_password.encode()).decode()
                )
        except Exception:
            logger.warning(
                "send_batch: could not decrypt password for SMTP %s", smtp_acc.id
            )

        smtp_config = {
            "host": smtp_acc.host,
            "port": smtp_acc.port,
            "username": smtp_acc.username,
            "password": smtp_password,
            "use_tls": smtp_acc.port == 587,
        }

        batch.started_at = datetime.utcnow()
        db.add(batch)
        db.commit()

        sent_count = 0

        # --- Step 4: Open persistent SMTP connection ---
        with SMTPClient(smtp_config) as client:
            for log in pending_logs:
                recipient = db.query(Recipient).filter(Recipient.id == log.recipient_id).first()
                if not recipient:
                    continue

                # Check SMTP sending limits
                if smtp_acc.daily_limit and (smtp_acc.used_today or 0) >= smtp_acc.daily_limit:
                    batch.paused = True
                    db.add(batch)
                    db.commit()
                    return {"status": "paused", "message": "Daily limit reached"}

                if smtp_acc.hourly_limit and (getattr(smtp_acc, "hourly_sent", 0) or 0) >= smtp_acc.hourly_limit:
                    batch.paused = True
                    db.add(batch)
                    db.commit()
                    return {"status": "paused", "message": "Hourly limit reached"}

                html_body = campaign.html_body
                text_body = campaign.text_body or "This message contains HTML content."

                try:
                    res = client.send(
                        to_address=recipient.email,
                        subject=campaign.subject,
                        html_body=html_body,
                        text_body=text_body,
                        from_name=campaign.from_name,
                        from_email=None,
                    )
                    status = "sent"
                    response_text = res.get("response") if isinstance(res, dict) else None
                    error_message = res.get("error") if isinstance(res, dict) else None
                except Exception as exc:
                    logger.exception("send_batch failed for %s: %s", recipient.email, exc)
                    status = "failed"
                    response_text = None
                    error_message = str(exc)
                    if self.request.retries < MAX_RETRIES:
                        raise self.retry(
                            exc=exc,
                            countdown=min(60 * (2 ** self.request.retries), 3600),
                        )

                # --- Update EmailLog ---
                log.status = status
                log.attempts += 1
                log.response = response_text
                log.error_message = error_message
                log.updated_at = datetime.utcnow()
                db.add(log)

                # --- Atomic Counter Updates ---
                batch.sent_count = (batch.sent_count or 0) + 1
                campaign.sent_count = (getattr(campaign, "sent_count", 0) or 0) + 1
                smtp_acc.used_today = (smtp_acc.used_today or 0) + 1
                smtp_acc.hourly_sent = (getattr(smtp_acc, "hourly_sent", 0) or 0) + 1

                db.add(batch)
                db.add(campaign)
                db.add(smtp_acc)
                db.commit()

                if status == "spam":
                    batch.paused = True
                    campaign.status = "paused"
                    campaign.seed_status = "spam"
                    db.add(batch)
                    db.add(campaign)
                    db.commit()
                    return {"status": "paused", "message": "Spam detected; campaign paused"}

                sent_count += 1
                time.sleep(0.12)

        # --- Step 5: Mark batch complete ---
        batch.completed_at = datetime.utcnow()
        db.add(batch)
        db.commit()

        # --- Step 6: Finalize campaign if all batches done ---
        remaining = (
            db.query(CampaignBatch)
            .filter(
                CampaignBatch.campaign_id == campaign.id,
                CampaignBatch.paused == False,
                CampaignBatch.completed_at == None,
            )
            .count()
        )
        if remaining == 0:
            campaign.status = "completed"
            db.add(campaign)
            db.commit()

        return {"status": "completed", "sent": sent_count}

    except Exception as exc:
        logger.exception("Unexpected error in send_batch %s: %s", batch_id, exc)
        try:
            batch = db.query(CampaignBatch).filter(CampaignBatch.id == batch_id).first()
            if batch:
                batch.paused = True
                db.add(batch)
                db.commit()
        except Exception:
            logger.exception("Failed to pause batch after error %s", batch_id)
        raise
    finally:
        db.close()