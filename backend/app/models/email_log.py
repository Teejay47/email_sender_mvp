from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Text, func
from sqlalchemy.orm import relationship
from .base import Base

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="SET NULL"), nullable=True, index=True)
    recipient_id = Column(Integer, ForeignKey("recipients.id", ondelete="SET NULL"), nullable=True, index=True)
    smtp_account_id = Column(Integer, ForeignKey("smtp_accounts.id", ondelete="SET NULL"), nullable=True, index=True)
    batch_id = Column(Integer, ForeignKey("campaign_batches.id", ondelete="SET NULL"), nullable=True, index=True)

    status = Column(String(50), nullable=True)
    attempts = Column(Integer, nullable=False, default=1)
    response = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    # relationships using string references
    campaign = relationship("Campaign", back_populates="email_logs")
    batch = relationship("CampaignBatch", back_populates="email_logs")
    recipient = relationship("Recipient", back_populates="email_logs")
    smtp_account = relationship("SMTPAccount", back_populates="email_logs")
