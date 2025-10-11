# backend/app/schemas/seedbox.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SeedBoxBase(BaseModel):
    email_address: str
    imap_host: Optional[str] = None
    imap_port: Optional[int] = None
    imap_username: Optional[str] = None
    imap_password: Optional[str] = None
    imap_use_ssl: Optional[bool] = True

    # ✅ Add these two new optional fields
    imap_inbox_folder: Optional[str] = "INBOX"
    imap_spam_folder: Optional[str] = "[Gmail]/Spam"


class SeedBoxCreate(SeedBoxBase):
    user_id: int

class SeedBoxOut(SeedBoxBase):
    id: int
    user_id: int
    last_status: Optional[str] = None
    last_checked: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
