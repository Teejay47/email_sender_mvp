from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base

class CampaignBatch(Base):
    __tablename__ = "campaign_batches"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"))
    smtp_account_id = Column(Integer, ForeignKey("smtp_accounts.id", ondelete="SET NULL"))
    seedbox_status = Column(String, nullable=True)
    sent_count = Column(Integer, default=0)
    total = Column(Integer, default=0)
    status = Column(String, default="pending")
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    campaign = relationship("Campaign", back_populates="batches")
    email_logs = relationship("EmailLog", back_populates="batch", cascade="all, delete-orphan")
