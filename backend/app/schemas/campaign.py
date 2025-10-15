# backend/app/schemas/campaign.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CampaignCreate(BaseModel):
    subject: str
    html_body: Optional[str] = None
    text_body: Optional[str] = None
    from_name: Optional[str] = None
    smtp_strategy: str = Field("round_robin")
    seed_check: bool = Field(True)

class CampaignListItem(BaseModel):
    id: int
    subject: str
    status: str
    created_at: datetime
    sent: int = 0
    total: int = 0
    seed_status: Optional[str] = None

    class Config:
        orm_mode = True

class EmailLogItem(BaseModel):
    id: int
    recipient_email: str
    status: str
    smtp_id: Optional[int]
    timestamp: datetime

    class Config:
        orm_mode = True
