# backend/app/schemas/smtp_account.py
from pydantic import BaseModel, IPvAnyAddress
from typing import Optional


class SMTPAccountCreate(BaseModel):
    host: str
    port: int = 587
    username: Optional[str]
    encrypted_password: Optional[str]
    daily_limit: Optional[int] = 0
    hourly_limit: Optional[int] = 0
