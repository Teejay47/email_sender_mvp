# backend/app/models/__init__.py
from .base import Base
from .user import User
from .smtp_account import SMTPAccount
from .recipient import Recipient
from .seedbox import SeedBox
from .campaign import Campaign
from .campaign_batch import CampaignBatch
from .email_log import EmailLog

__all__ = [
    "Base",
    "User",
    "SMTPAccount",
    "Recipient",
    "SeedBox",
    "Campaign",
    "CampaignBatch",
    "EmailLog",
]

