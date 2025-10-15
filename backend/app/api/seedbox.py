# backend/app/api/seedbox.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from datetime import datetime
import logging
import random

from app.core.database import get_db
from app.models.seedbox import SeedBox
from app.models.smtp_account import SMTPAccount
from app.schemas.seedbox import SeedBoxOut
from app.tasks.seedbox_tasks import send_seed_test_task
from app.utils.email_sender import send_email
from app.core.config import settings
from app.schemas.seedbox import SeedBoxOut, SeedBoxCreate  # ✅ Include SeedBoxCreate
from app.core.security import fernet


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/seedbox", tags=["seedbox"])




@router.post("/add", response_model=SeedBoxOut)
def add_seedbox(data: SeedBoxCreate, db: Session = Depends(get_db)):
    encrypted_pw = (
        fernet.encrypt(data.imap_password.encode()).decode()
        if data.imap_password
        else None
    )

    obj = SeedBox(
        user_id=data.user_id,
        email_address=data.email_address.strip().lower(),
        imap_host=data.imap_host,
        imap_port=data.imap_port,
        imap_username=data.imap_username,
        imap_encrypted_password=encrypted_pw,
        imap_use_ssl=data.imap_use_ssl,
        imap_inbox_folder=data.imap_inbox_folder,  # ✅ new
        imap_spam_folder=data.imap_spam_folder,  # ✅ new
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)
    logger.info(f"Added seedbox for user {data.user_id}: {data.email_address}")
    return obj




@router.get("/list", response_model=List[SeedBoxOut])
def list_seedboxes(user_id: int = 1, db: Session = Depends(get_db)):

    qs = db.query(SeedBox).filter(SeedBox.user_id == user_id).order_by(SeedBox.id.desc()).all()
    return qs


@router.delete("/{seedbox_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seedbox(seedbox_id: int, db: Session = Depends(get_db)):
    obj = db.query(SeedBox).filter(SeedBox.id == seedbox_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Seed box not found")
    db.delete(obj)
    db.commit()
    return {"detail": "deleted"}


@router.post("/test")
def test_seedbox(seedbox_id: int = Body(...), user_id: int = Body(1), db: Session = Depends(get_db)):
    seedbox = db.query(SeedBox).filter(SeedBox.id == seedbox_id, SeedBox.user_id == int(user_id)).first()
    if not seedbox:
        raise HTTPException(status_code=404, detail="Seed box not found")

    smtp = db.query(SMTPAccount).filter(SMTPAccount.user_id == int(user_id), SMTPAccount.is_active == True).first()
    if not smtp:
        raise HTTPException(status_code=400, detail="No SMTP account available for sending test")

    try:
        subject = f"[Seed Test] Inbox check - {datetime.utcnow().isoformat()}"
        body = f"This is a seed inbox placement test sent to {seedbox.email_address}."

        send_email(
            smtp_config={
                "host": smtp.host or settings.SMTP_HOST,
                "port": smtp.port or settings.SMTP_PORT,
                "username": smtp.username or settings.SMTP_USERNAME,
                "password": smtp.encrypted_password or settings.SMTP_PASSWORD,
                "use_tls": smtp.port == 587,
            },
            to_address=seedbox.email_address,
            subject=subject,
            text_body=body,
            from_name=settings.FROM_NAME,
            from_email=settings.FROM_EMAIL,
            reply_to=settings.REPLY_TO,
        )

        # 🧠 Real IMAP inbox check
        from app.utils.imap_checker import check_inbox_placement

        imap_password = None
        if seedbox.imap_encrypted_password:
            try:
                imap_password = fernet.decrypt(seedbox.imap_encrypted_password.encode()).decode()
            except Exception:
                logger.warning("Could not decrypt IMAP password for seedbox %s", seedbox.id)

        imap_config = {
            "host": seedbox.imap_host,
            "port": seedbox.imap_port or 993,
            "username": seedbox.imap_username,
            "password": imap_password,
            "use_ssl": seedbox.imap_use_ssl,
            "inbox_folder": seedbox.imap_inbox_folder,  # ✅ new
            "spam_folder": seedbox.imap_spam_folder,  # ✅ new
        }

        result = check_inbox_placement(imap_config, subject_keyword=subject)

        # Save result
        seedbox.last_status = result
        seedbox.last_checked = datetime.utcnow()
        db.add(seedbox)
        db.commit()
        db.refresh(seedbox)

        logger.info("Seed test for %s returned: %s", seedbox.email_address, result)
        return {
            "id": seedbox.id,
            "email_address": seedbox.email_address,
            "user_id": seedbox.user_id,
            "last_status": seedbox.last_status,
            "last_checked": seedbox.last_checked,
            "created_at": seedbox.created_at,
            "updated_at": seedbox.updated_at,
            "result": seedbox.last_status,
        }

    except Exception as exc:
        logger.exception("Failed to send seed test")
        raise HTTPException(status_code=500, detail=str(exc))



@router.post("/test/async")
def test_seedbox_async(seedbox_id: int = Body(...), user_id: int = Body(1)):
    """
    Queue an asynchronous seed test via Celery.
    """
    task = send_seed_test_task.delay(int(seedbox_id), int(user_id))
    return {"status": "queued", "task_id": task.id}
