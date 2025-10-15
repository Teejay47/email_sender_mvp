# backend/app/app/api/campaigns.py
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Body, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging

from app.core.database import get_db
from app.models.campaign import Campaign
from app.models.campaign_batch import CampaignBatch
from app.models.smtp_account import SMTPAccount
from app.models.recipient import Recipient
from app.models.email_log import EmailLog
from app.models.seedbox import SeedBox
from app.tasks.campaign_tasks import send_batch
from app.utils.imap_checker import check_inbox_placement
from app.utils.email_sender import send_email
from app.core.config import settings
from app.core.security import fernet

logger = logging.getLogger(__name__)
router = APIRouter(tags=["campaigns"])


class CampaignCreateSchema(BaseModel):
    subject: str
    html_body: str
    text_body: Optional[str] = None
    from_name: Optional[str] = None
    smtp_strategy: str = "round_robin"  # or 'single'
    seed_check: bool = True


class CampaignListItem(BaseModel):
    id: int
    subject: str
    status: str
    sent_count: int
    total_recipients: int
    seed_status: Optional[str]
    created_at: datetime
    updated_at: datetime


@router.post("/create")
def create_campaign(data: CampaignCreateSchema, db: Session = Depends(get_db)):
    # Create a new campaign entry
    new_campaign = Campaign(
        subject=data.subject,
        html_body=data.html_body,
        text_body=data.text_body,
        from_name=data.from_name,
        smtp_strategy=data.smtp_strategy,
        seed_check=data.seed_check,
        status="draft",
        sent_count=0,
        total_recipients=0,
        seed_status=None,
        user_id=1,  # 👈 temporary hardcoded user

        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    return {
        "id": new_campaign.id,
        "message": "Campaign created successfully",
        "status": new_campaign.status,
    }


@router.post("/start/{campaign_id}")
def start_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign: Campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if campaign.status == "running":
        return {"status": "running", "message": "Campaign already running"}

    # Recipients for campaign
    all_recipients = db.query(Recipient).filter(
        Recipient.validated == True,
        Recipient.suppressed == False
    ).all()
    total_recipients = len(all_recipients)
    if total_recipients == 0:
        raise HTTPException(status_code=400, detail="No recipients to send to")

    campaign.total_recipients = total_recipients
    db.add(campaign)
    db.commit()

    # Fetch active SMTP accounts
    smtp_accounts: List[SMTPAccount] = db.query(SMTPAccount).filter(
        SMTPAccount.is_active == True
    ).order_by(SMTPAccount.id).all()
    if not smtp_accounts:
        raise HTTPException(status_code=400, detail="No active SMTP accounts available")

    # Build batches
    created_batches = []
    idx = 0
    for smtp in smtp_accounts:
        limit = smtp.daily_limit if smtp.daily_limit and smtp.daily_limit > 0 else 500
        while idx < total_recipients:
            chunk = all_recipients[idx: idx + limit]
            if not chunk:
                break

            batch = CampaignBatch(
                campaign_id=campaign.id,
                smtp_account_id=smtp.id,
                batch_number=len(created_batches) + 1,
                recipients_count=len(chunk),
                seedbox_status="unknown",
                sent_count=0,
                paused=False,
                created_at=datetime.utcnow(),
            )
            db.add(batch)
            db.commit()
            db.refresh(batch)

            # Auto-create EmailLog entries
            for r in chunk:
                log = EmailLog(
                    campaign_id=campaign.id,
                    recipient_id=r.id,
                    batch_id=batch.id,
                    smtp_account_id=smtp.id,
                    status="pending",
                    attempts=0,
                    timestamp=datetime.utcnow(),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(log)
            db.commit()

            created_batches.append(batch)
            idx += limit
            break

    if not created_batches:
        raise HTTPException(status_code=500, detail="Failed to create batches")

    # Fetch seedboxes for user
    seedboxes: List[SeedBox] = db.query(SeedBox).filter(
        SeedBox.user_id == 1
    ).order_by(SeedBox.id).all()
    if not seedboxes and campaign.seed_check:
        campaign.status = "paused"
        campaign.seed_status = "not_found"
        db.add(campaign)
        db.commit()
        return {"status": "paused", "message": "No seedbox configured; campaign paused"}

    any_paused = False
    smtp_errors = []

    for batch in created_batches:
        if not campaign.seed_check:
            send_batch.delay(batch.id)
            continue

        # Try each SMTP account until one works
        smtp_used = None
        for smtp in smtp_accounts:
            if not smtp.is_active:
                continue

            # Try decrypting, fallback to plain text
            smtp_password = None
            if smtp.encrypted_password:
                try:
                    smtp_password = fernet.decrypt(smtp.encrypted_password.encode()).decode()
                except Exception:
                    smtp_password = smtp.encrypted_password

            smtp_config = {
                "host": smtp.host or settings.SMTP_HOST,
                "port": smtp.port or settings.SMTP_PORT,
                "username": smtp.username,
                "password": smtp_password,
                "use_tls": smtp.port == 587,
            }

            try:
                # Dry-run test connection (accept None to skip actual send)
                send_email(
                    smtp_config=smtp_config,
                    to_address=None,
                    subject="SMTP test",
                    html_body="Test",
                    text_body="Test",
                    from_name=campaign.from_name or settings.FROM_NAME,
                    from_email=settings.FROM_EMAIL,
                    reply_to=settings.REPLY_TO,
                    test_mode=True
                )
                smtp_used = smtp
                break
            except Exception as exc:
                smtp_errors.append(f"SMTP {smtp.id}: {smtp.username}@{smtp.host} -> {str(exc)}")
                continue

        if not smtp_used:
            batch.paused = True
            campaign.status = "paused"
            campaign.seed_status = "no_working_smtp"
            db.add(batch)
            db.add(campaign)
            db.commit()
            any_paused = True
            break

        # Try each seedbox until one works
        seed_success = False
        for seedbox in seedboxes:
            subject = f"[Seed Test] Campaign {campaign.id} - {datetime.utcnow().isoformat()}"
            html_body = f"<p>Seed test for campaign {campaign.id} sent to {seedbox.email_address}</p>"
            text_body = f"Seed test for campaign {campaign.id} sent to {seedbox.email_address}"

            try:
                send_email(
                    smtp_config={
                        "host": smtp_used.host,
                        "port": smtp_used.port,
                        "username": smtp_used.username,
                        "password": smtp_password,
                        "use_tls": smtp_used.port == 587,
                    },
                    to_address=seedbox.email_address,
                    subject=subject,
                    html_body=html_body,
                    text_body=text_body,
                    from_name=campaign.from_name or settings.FROM_NAME,
                    from_email=settings.FROM_EMAIL,
                    reply_to=settings.REPLY_TO,
                )
            except Exception as exc:
                smtp_errors.append(f"Seedbox {seedbox.id} failed with SMTP {smtp_used.id}: {str(exc)}")
                continue

            # IMAP check
            imap_password = None
            if seedbox.imap_encrypted_password:
                try:
                    imap_password = fernet.decrypt(seedbox.imap_encrypted_password.encode()).decode()
                except Exception:
                    continue

            imap_config = {
                "host": seedbox.imap_host,
                "port": seedbox.imap_port or 993,
                "username": seedbox.imap_username,
                "password": imap_password,
                "use_ssl": seedbox.imap_use_ssl,
                "inbox_folder": seedbox.imap_inbox_folder,
                "spam_folder": seedbox.imap_spam_folder,
            }

            seed_result = check_inbox_placement(imap_config, subject_keyword=subject)
            batch.seedbox_status = seed_result
            db.add(batch)
            db.commit()

            if seed_result == "inbox":
                seed_success = True
                send_batch.delay(batch.id)
                break

        if not seed_success:
            campaign.status = "paused"
            campaign.seed_status = "failed_all"
            db.add(campaign)
            db.commit()
            any_paused = True
            break

    if not any_paused:
        campaign.status = "running"
        db.add(campaign)
        db.commit()
        return {"status": "running", "message": "Campaign started"}
    else:
        return {
            "status": campaign.status,
            "message": "Campaign paused; all seedboxes or SMTP failed",
            "seed_status": campaign.seed_status,
            "smtp_errors": smtp_errors
        }

@router.get("/list", response_model=List[CampaignListItem])
def list_campaigns(db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).order_by(Campaign.created_at.desc()).all()
    result = []
    for c in campaigns:
        result.append(
            CampaignListItem(
                id=c.id,
                subject=c.subject,
                status=c.status,
                sent_count=getattr(c, "sent_count", 0) or 0,
                total_recipients=getattr(c, "total_recipients", 0) or 0,
                seed_status=getattr(c, "seed_status", None),
                created_at=c.created_at,
                updated_at=c.updated_at,
            )
        )
    return result


@router.get("/{campaign_id}/logs")
def get_campaign_logs(
    campaign_id: int,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 50,
    db: Session = Depends(get_db),
):
    q = db.query(EmailLog).filter(EmailLog.campaign_id == campaign_id)
    if status:
        q = q.filter(EmailLog.status == status)

    total = q.count()
    logs = (
        q.order_by(EmailLog.timestamp.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    items = []
    for l in logs:
        items.append({
            "id": getattr(l, "id", None),
            "recipient": getattr(l.recipient, "email", None) if l.recipient else None,
            "status": getattr(l, "status", None),
            "timestamp": getattr(l, "timestamp", None),
            "response": getattr(l, "response", None),
            "smtp_account_id": getattr(l, "smtp_account_id", None),
            "batch_id": getattr(l, "batch_id", None),
            "attempts": getattr(l, "attempts", None),           # ✅ number of send attempts
            "error_message": getattr(l, "error_message", None), # ✅ last error if send failed
        })

    return {"total": total, "page": page, "page_size": page_size, "items": items}
