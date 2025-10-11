# backend/app/tasks/recipient_tasks.py
from app.celery_worker import celery
from typing import List
from app.core.database import get_db
from app.models.recipient import Recipient
from app.utils.validators import is_valid_email


@celery.task(bind=True)
def import_recipients_task(self, emails: List[str], user_id: int):
    """
    Simple Celery task to import recipients. Reports minimal progress via task meta.
    """
    total = len(emails)
    valid_count = 0
    invalid_count = 0

    # we must create a DB session here (don't use FastAPI dependency)
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        for i, email in enumerate(emails):
            try:
                normalized = email.strip().lower()
                valid = is_valid_email(normalized)
                suppressed = not valid
                obj = db.query(Recipient).filter(Recipient.user_id == user_id, Recipient.email == normalized).first()
                if obj:
                    obj.validated = valid
                    obj.suppressed = suppressed
                else:
                    obj = Recipient(user_id=user_id, email=normalized, validated=valid, suppressed=suppressed)
                    db.add(obj)
                if valid:
                    valid_count += 1
                else:
                    invalid_count += 1
                if i % 20 == 0:
                    db.commit()
                self.update_state(state="PROGRESS", meta={"processed": i + 1, "total": total})
            except Exception as e:
                # continue on errors
                continue
        db.commit()
    finally:
        db.close()
    return {"total": total, "valid": valid_count, "invalid": invalid_count}




@celery.task(bind=True)
def bulk_delete_recipients_task(self, user_id: int, target: str = "all"):
    """
    Celery background task for bulk deleting recipients.
    """
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        qs = db.query(Recipient).filter(Recipient.user_id == user_id)
        if target == "invalid":
            qs = qs.filter(Recipient.validated == False)
        elif target == "suppressed":
            qs = qs.filter(Recipient.suppressed == True)

        count = qs.count()
        qs.delete(synchronize_session=False)
        db.commit()
        return {"deleted": count, "target": target, "status": "completed"}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
