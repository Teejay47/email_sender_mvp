# /backend/app/api/smtp.py
from typing import List, Optional
import smtplib
import logging
import os

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.smtp_account import SMTPAccount
from app.schemas.smtp_account import SMTPAccountCreate, SMTPAccountRead, SMTPAccountUpdate

from cryptography.fernet import Fernet, InvalidToken
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/smtp", tags=["smtp"])


# ---------------------------------------------------------------------------
# 🔐 Encryption helpers
# ---------------------------------------------------------------------------
def get_fernet() -> Fernet:
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        print("❌ ENCRYPTION_KEY missing at runtime!")  # visible in docker logs
        raise RuntimeError("ENCRYPTION_KEY is not set in environment")
    key = key.strip()
    try:
        return Fernet(key.encode())
    except Exception as e:
        print(f"❌ Invalid ENCRYPTION_KEY format: {e}")
        raise RuntimeError(f"Invalid ENCRYPTION_KEY: {e}")


def encrypt_password(plain: Optional[str]) -> str:
    if not plain:
        raise ValueError("Cannot encrypt an empty or null password")
    f = get_fernet()
    token = f.encrypt(plain.encode())
    return token.decode()


def decrypt_password(token: str) -> str:
    f = get_fernet()
    try:
        return f.decrypt(token.encode()).decode()
    except InvalidToken:
        raise ValueError("Invalid encryption token")


# ---------------------------------------------------------------------------
# 🩺 Health route (placed BEFORE dynamic routes)
# ---------------------------------------------------------------------------
@router.get("/_health")
def smtp_module_health(db: Session = Depends(get_db)):
    return {
        "db": "ok",
        "encryption": "ENCRYPTION_KEY set" if os.getenv("ENCRYPTION_KEY") else "ENCRYPTION_KEY missing"
    }


# ---------------------------------------------------------------------------
# 📦 CRUD Endpoints
# ---------------------------------------------------------------------------
@router.post("/add", response_model=SMTPAccountRead, status_code=status.HTTP_201_CREATED)
def add_smtp(payload: SMTPAccountCreate, db: Session = Depends(get_db)):
    if not payload.password:
        raise HTTPException(status_code=400, detail="Password is required")

    try:
        encrypted_pw = encrypt_password(payload.password)
    except Exception as e:
        logger.exception("Failed to encrypt SMTP password: %s", e)
        raise HTTPException(status_code=500, detail=f"Encryption failed: {e}")

    smtp = SMTPAccount(
        user_id=payload.user_id,
        host=payload.host,
        port=payload.port,
        username=payload.username,
        encrypted_password=encrypted_pw,
        daily_limit=payload.daily_limit,
        hourly_limit=payload.hourly_limit,
        status=payload.status or "unknown",
        is_active=payload.is_active if payload.is_active is not None else True,
    )

    db.add(smtp)
    db.commit()
    db.refresh(smtp)
    return smtp


@router.get("/list", response_model=List[SMTPAccountRead])
def list_smtps(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    qs = db.query(SMTPAccount)
    if user_id:
        qs = qs.filter(SMTPAccount.user_id == user_id)
    return qs.all()


@router.get("/{smtp_id}", response_model=SMTPAccountRead)
def get_smtp(smtp_id: int, db: Session = Depends(get_db)):
    smtp = db.query(SMTPAccount).filter(SMTPAccount.id == smtp_id).first()
    if not smtp:
        raise HTTPException(status_code=404, detail="SMTP account not found")
    return smtp


@router.put("/{smtp_id}", response_model=SMTPAccountRead)
def update_smtp(smtp_id: int, payload: SMTPAccountUpdate, db: Session = Depends(get_db)):
    smtp = db.query(SMTPAccount).filter(SMTPAccount.id == smtp_id).first()
    if not smtp:
        raise HTTPException(status_code=404, detail="SMTP account not found")

    for name, val in payload.dict(exclude_unset=True).items():
        if name == "password" and val:
            setattr(smtp, "encrypted_password", encrypt_password(val))
        elif val is not None:
            setattr(smtp, name, val)

    db.add(smtp)
    db.commit()
    db.refresh(smtp)
    return smtp


@router.delete("/{smtp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_smtp(smtp_id: int, db: Session = Depends(get_db)):
    smtp = db.query(SMTPAccount).filter(SMTPAccount.id == smtp_id).first()
    if not smtp:
        raise HTTPException(status_code=404, detail="SMTP account not found")
    db.delete(smtp)
    db.commit()
    return {"detail": "deleted"}


# ---------------------------------------------------------------------------
# ✉️ Test Connection
# ---------------------------------------------------------------------------
class TestConnectionPayload(BaseModel):
    smtp_id: Optional[int] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    use_ssl: Optional[bool] = False
    test_recipient: Optional[str] = None


@router.post("/test")
def test_connection(payload: TestConnectionPayload, db: Session = Depends(get_db)):
    host = payload.host
    port = payload.port
    username = payload.username
    password = payload.password
    use_ssl = payload.use_ssl

    if payload.smtp_id:
        smtp = db.query(SMTPAccount).filter(SMTPAccount.id == payload.smtp_id).first()
        if not smtp:
            raise HTTPException(status_code=404, detail="SMTP account not found")
        host = smtp.host
        port = smtp.port
        username = smtp.username
        try:
            password = decrypt_password(smtp.encrypted_password)
        except Exception:
            logger.exception("Failed to decrypt SMTP password")
            raise HTTPException(status_code=500, detail="Failed to decrypt password")

    if not all([host, port, username, password]):
        raise HTTPException(status_code=400, detail="Missing SMTP credentials")

    try:
        if use_ssl or port == 465:
            server = smtplib.SMTP_SSL(host=host, port=port, timeout=10)
        else:
            server = smtplib.SMTP(host=host, port=port, timeout=10)
            server.starttls()
        server.login(username, password)
        if payload.test_recipient:
            from email.message import EmailMessage
            msg = EmailMessage()
            msg["Subject"] = "SMTP Manager Test"
            msg["From"] = username
            msg["To"] = payload.test_recipient
            msg.set_content("This is a test message from Email Sender MVP SMTP Manager.")
            server.send_message(msg)
        server.quit()
        return {"status": "success"}
    except smtplib.SMTPAuthenticationError as e:
        logger.warning("SMTP auth failed: %s", e)
        return {"error": "auth_failed", "detail": str(e)}
    except Exception as e:
        logger.exception("SMTP connection failed")
        raise HTTPException(status_code=500, detail=f"connection_failed: {e}")
