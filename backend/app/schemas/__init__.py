# backend/app/schemas/__init__.py
# expose schemas easily
from .user import UserCreate  # noqa: F401
from .smtp_account import SMTPAccountCreate  # noqa: F401
from .recipient import RecipientCreate  # noqa: F401
from .campaign import CampaignCreate  # noqa: F401
