# backend/app/schemas/campaign.py
from pydantic import BaseModel
from typing import Optional


class CampaignCreate(BaseModel):
    subject: str
    html_body: Optional[str] = None
    text_body: Optional[str] = None
    from_name: Optional[str] = None
