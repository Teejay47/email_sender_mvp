# backend/app/models/campaign_batch.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from .base import Base


class CampaignBatch(Base):
    __tablename__ = "campaign_batches"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"))
    smtp_account_id = Column(Integer, ForeignKey("smtp_accounts.id", ondelete="SET NULL"))
    batch_number = Column(Integer, nullable=True)
    seedbox_status = Column(String, nullable=True)
    sent_count = Column(Integer, default=0)
    recipients_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="pending")
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    paused = Column(Boolean, default=False)

    # relationships using string references
    campaign = relationship("Campaign", back_populates="batches")
    smtp_account = relationship("SMTPAccount", back_populates="batches")
    email_logs = relationship("EmailLog", back_populates="batch", cascade="all, delete-orphan")
