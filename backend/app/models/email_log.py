# backend/app/models/email_log.py
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship

from .base import Base


class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="SET NULL"), nullable=True, index=True)
    recipient_id = Column(Integer, ForeignKey("recipients.id", ondelete="SET NULL"), nullable=True, index=True)
    smtp_id = Column(Integer, ForeignKey("smtp_accounts.id", ondelete="SET NULL"), nullable=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="SET NULL"), nullable=True, index=True)

    status = Column(String(50), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    response = Column(String, nullable=True)  # optional store provider response

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    campaign = relationship("Campaign", back_populates="email_logs")
    recipient = relationship("Recipient", back_populates="email_logs")
    smtp_account = relationship("SMTPAccount")
    batch = relationship("Batch", back_populates="email_logs")
