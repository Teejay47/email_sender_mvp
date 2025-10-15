# backend/app/models/campaign.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, ForeignKey, event
from sqlalchemy.orm import relationship
from .base import Base  # Base declarative class


class Campaign(Base):
    __tablename__ = "campaigns"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)  # 👈 now nullable
    subject = Column(String, nullable=False)
    html_body = Column(Text, nullable=False)
    text_body = Column(Text, nullable=True)
    from_name = Column(String, nullable=True)
    smtp_strategy = Column(String, default="round_robin")
    seed_check = Column(Boolean, default=True)
    status = Column(String, default="draft")
    sent_count = Column(Integer, default=0)
    total_recipients = Column(Integer, default=0)
    seed_status = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="campaigns")

    batches = relationship("CampaignBatch", back_populates="campaign", cascade="all, delete-orphan")
    email_logs = relationship("EmailLog", back_populates="campaign", cascade="all, delete-orphan")


# Automatically set campaign name to subject if not provided
@event.listens_for(Campaign, "before_insert")
def auto_fill_name(mapper, connection, target):
    if not target.name:
        target.name = target.subject
