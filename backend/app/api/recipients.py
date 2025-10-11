# backend/app/api/recipients.py
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Body
from sqlalchemy.orm import Session
import csv
import io
import logging

from app.core.database import get_db
from app.models.recipient import Recipient
from app.schemas.recipient import RecipientOut  # ensure this exists
from app.utils.validators import is_valid_email, check_mx_record
from app.tasks.recipient_tasks import import_recipients_task  # optional async import
from app.tasks.recipient_tasks import import_recipients_task, bulk_delete_recipients_task  # add new import
from fastapi import Query


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/recipients", tags=["recipients"])


def _normalize_email(email: str) -> str:
    return email.strip().lower()


@router.post("/import")
def import_recipients(
    file: Optional[UploadFile] = File(None),
    pasted: Optional[str] = Form(None),
    user_id: int = Form(1),
    async_task: Optional[bool] = Form(False),
    db: Session = Depends(get_db),
):
    """
    Accepts CSV, TXT upload, or pasted list of emails.
    Saves directly to DB with validation and deduplication.
    """
    emails = []

    if file:
        content = file.file.read().decode(errors="ignore").strip()
        filename = file.filename.lower()

        if filename.endswith(".csv"):
            reader = csv.reader(io.StringIO(content))
            for row in reader:
                if not row:
                    continue
                emails.append(row[0].strip())

        elif filename.endswith(".txt"):
            raw = content.replace(",", "\n").replace(";", "\n")
            for line in raw.splitlines():
                v = line.strip()
                if v:
                    emails.append(v)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type (only .csv or .txt accepted)")

    elif pasted:
        raw = pasted.replace(",", "\n").replace(";", "\n")
        for line in raw.splitlines():
            v = line.strip()
            if v:
                emails.append(v)
    else:
        raise HTTPException(status_code=400, detail="No file or pasted data provided")

    # Normalize and deduplicate
    normalized = {_normalize_email(e) for e in emails if e}
    total = len(normalized)
    if total == 0:
        return {"total": 0, "valid_count": 0, "invalid_count": 0, "details": []}

    logger.warning(f"🟡 Starting import of {total} recipients (user_id={user_id})")

    if async_task:
        task_id = import_recipients_task.delay(list(normalized), int(user_id)).id
        return {"status": "queued", "task_id": task_id, "total": total}

    valid_count = 0
    invalid_count = 0
    details = []

    for email in normalized:
        valid = False
        suppressed = False
        try:
            valid = is_valid_email(email)
            if valid:
                try:
                    has_mx = check_mx_record(email)
                    if has_mx is False:
                        logger.debug(f"No MX record for {email}")
                except Exception:
                    logger.debug(f"MX check failed for {email}", exc_info=True)
            else:
                suppressed = True
        except Exception as e:
            logger.exception(f"Validation error for {email}: {e}")
            valid = False
            suppressed = True

        obj = db.query(Recipient).filter(
            Recipient.user_id == user_id,
            Recipient.email == email
        ).first()

        if obj:
            obj.validated = bool(valid)
            obj.suppressed = bool(suppressed)
        else:
            obj = Recipient(
                user_id=int(user_id),
                email=email,
                validated=bool(valid),
                suppressed=bool(suppressed),
            )
            db.add(obj)

        if valid:
            valid_count += 1
        else:
            invalid_count += 1

        details.append({
            "email": email,
            "validated": bool(valid),
            "suppressed": bool(suppressed),
        })

    logger.warning(f"🟢 Committing {len(details)} recipients to DB...")
    try:
        db.flush()
        db.commit()
        logger.warning("✅ Commit successful!")
    except Exception as e:
        logger.exception(f"❌ Commit failed: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database commit failed")
    finally:
        db.close()

    return {
        "total": total,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "details": details,
    }



@router.get("/list", response_model=List[RecipientOut])
def list_recipients(
    page: int = 1,
    per_page: int = 50,
    filter_status: Optional[str] = None,  # values: 'valid', 'suppressed', or None
    user_id: int = 1,  # placeholder for auth
    db: Session = Depends(get_db),
):
    qs = db.query(Recipient).filter(Recipient.user_id == user_id)
    if filter_status == "valid":
        qs = qs.filter(Recipient.validated == True, Recipient.suppressed == False)
    elif filter_status == "suppressed":
        qs = qs.filter(Recipient.suppressed == True)

    total = qs.count()
    items = qs.order_by(Recipient.id.desc()).offset((page - 1) * per_page).limit(per_page).all()

    # We return list (fastapi will use response_model)
    return items


@router.put("/{recipient_id}/suppress")
def suppress_recipient(recipient_id: int, suppressed: bool = Body(...), db: Session = Depends(get_db)):
    obj = db.query(Recipient).filter(Recipient.id == recipient_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Recipient not found")
    obj.suppressed = bool(suppressed)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"id": obj.id, "email": obj.email, "suppressed": obj.suppressed}


@router.delete("/{recipient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipient(recipient_id: int, db: Session = Depends(get_db)):
    obj = db.query(Recipient).filter(Recipient.id == recipient_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Recipient not found")
    db.delete(obj)
    db.commit()
    return {"detail": "deleted"}


@router.delete("/bulk", status_code=status.HTTP_200_OK)
def bulk_delete_recipients(
    target: str = Query("all", description="Target type: all, invalid, suppressed"),
    async_task: bool = Query(False, description="Run deletion asynchronously"),
    user_id: int = Query(1, description="User ID placeholder"),
    db: Session = Depends(get_db),
):

    """
    Bulk delete recipients by target type.
    - target: 'all', 'invalid', or 'suppressed'
    - async_task: if True, run deletion as a Celery background task
    """
    valid_targets = {"all", "invalid", "suppressed"}
    if target not in valid_targets:
        raise HTTPException(status_code=400, detail=f"Invalid target type '{target}'")

    # If async deletion requested
    if async_task:
        task = bulk_delete_recipients_task.delay(user_id=user_id, target=target)
        return {"status": "queued", "task_id": task.id, "target": target}

    # Otherwise, run synchronous delete
    qs = db.query(Recipient).filter(Recipient.user_id == user_id)
    if target == "invalid":
        qs = qs.filter(Recipient.validated == False)
    elif target == "suppressed":
        qs = qs.filter(Recipient.suppressed == True)

    count = qs.count()
    if count == 0:
        return {"deleted": 0, "target": target, "message": "No recipients matched"}

    qs.delete(synchronize_session=False)
    db.commit()
    return {"deleted": count, "target": target, "message": "Recipients deleted"}
