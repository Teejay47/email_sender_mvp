# backend/app/utils/campaign_helpers.py
from app.models import SMTPAccount, Recipient, CampaignBatch, EmailLog, Campaign
from app.core.database import SessionLocal
from datetime import datetime
import math
import random
from typing import List, Dict

db = SessionLocal()

def split_recipients_into_batches(
    campaign_id: int,
    user_id: int,
    batch_size: int = None,          # optional fixed number per batch
    smtp_strategy: str = "round_robin"
) -> List[Dict]:
    """
    Splits recipients into batches according to SMTP strategy and limits.
    Returns list of dicts with 'batch' and 'recipients'.
    """
    campaign = db.query(Campaign).filter_by(id=campaign_id, user_id=user_id).first()
    if not campaign:
        raise ValueError("Campaign not found.")

    # Get active SMTPs
    smtps: List[SMTPAccount] = db.query(SMTPAccount).filter_by(user_id=user_id, is_active=True).all()
    if not smtps:
        raise ValueError("No active SMTP accounts.")

    # Get recipients
    recipients: List[Recipient] = db.query(Recipient).filter(
        Recipient.user_id==user_id,
        Recipient.validated==True,
        Recipient.suppressed==False
    ).all()
    if not recipients:
        raise ValueError("No valid recipients.")

    # Shuffle for randomness
    random.shuffle(recipients)

    # Decide batch splitting
    batches_created = []

    if smtp_strategy == "round_robin":
        # divide recipients evenly among SMTPs
        num_smtp = len(smtps)
        for idx, smtp in enumerate(smtps):
            smtp_recipients = recipients[idx::num_smtp]  # distribute
            if batch_size:
                # split further into smaller batches
                chunks = [smtp_recipients[i:i+batch_size] for i in range(0, len(smtp_recipients), batch_size)]
            else:
                chunks = [smtp_recipients]

            for chunk in chunks:
                batch = CampaignBatch(
                    campaign_id=campaign.id,
                    smtp_account_id=smtp.id,
                    seedbox_status="pending",
                    sent_count=0,
                    total=len(chunk),
                    status="pending",
                    started_at=None,
                    completed_at=None
                )
                db.add(batch)
                db.commit()
                db.refresh(batch)
                # create email logs
                for r in chunk:
                    email_log = EmailLog(
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
                    db.add(email_log)
                db.commit()
                batches_created.append({"batch": batch, "recipients": chunk})

    elif smtp_strategy == "fixed_batch":
        # chunk all recipients by batch_size and assign to SMTPs in round-robin
        if not batch_size:
            batch_size = 50  # default
        chunks = [recipients[i:i+batch_size] for i in range(0, len(recipients), batch_size)]
        for idx, chunk in enumerate(chunks):
            smtp = smtps[idx % len(smtps)]
            batch = CampaignBatch(
                campaign_id=campaign.id,
                smtp_account_id=smtp.id,
                seedbox_status="pending",
                sent_count=0,
                total=len(chunk),
                status="pending"
            )
            db.add(batch)
            db.commit()
            db.refresh(batch)
            for r in chunk:
                email_log = EmailLog(
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
                db.add(email_log)
            db.commit()
            batches_created.append({"batch": batch, "recipients": chunk})

    else:
        raise ValueError("Unsupported SMTP strategy.")

    return batches_created
