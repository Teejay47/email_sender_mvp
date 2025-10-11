# backend/app/schemas/smtp_account.py
from pydantic import BaseModel, ConfigDict
from typing import Optional


class SMTPAccountBase(BaseModel):
    host: str
    port: int
    username: Optional[str] = None
    daily_limit: Optional[int] = 0
    hourly_limit: Optional[int] = 0
    status: Optional[str] = "new"
    is_active: Optional[bool] = True


class SMTPAccountCreate(SMTPAccountBase):
    user_id: int
    password: Optional[str] = None  # plain password sent from client


class SMTPAccountUpdate(BaseModel):
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    daily_limit: Optional[int] = None
    hourly_limit: Optional[int] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None


class SMTPAccountRead(SMTPAccountBase):
    id: int
    user_id: int
    used_today: int
    last_reset: Optional[str] = None

    # ✅ Modern Pydantic v2 syntax
    model_config = ConfigDict(from_attributes=True)
