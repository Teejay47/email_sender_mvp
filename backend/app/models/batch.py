# backend/app/models/batch.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from .base import Base


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False, index=True)
    smtp_id = Column(Integer, ForeignKey("smtp_accounts.id", ondelete="SET NULL"), nullable=True, index=True)

    batch_number = Column(Integer, nullable=False, default=0)
    seedbox_status = Column(String(100), nullable=True)
    sent_count = Column(Integer, nullable=False, default=0)
    paused = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    campaign = relationship("Campaign", back_populates="batches")
    smtp_account = relationship("SMTPAccount", back_populates="batches")
    email_logs = relationship("EmailLog", back_populates="batch")
