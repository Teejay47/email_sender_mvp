# backend/app/models/smtp_account.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from .base import Base


class SMTPAccount(Base):
    __tablename__ = "smtp_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False, default=587)
    username = Column(String(255), nullable=True)
    encrypted_password = Column(String, nullable=True)
    daily_limit = Column(Integer, nullable=True, default=0)
    hourly_limit = Column(Integer, nullable=True, default=0)
    status = Column(String(50), nullable=True)
    used_today = Column(Integer, nullable=False, default=0)
    last_reset = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="smtp_accounts")
    batches = relationship("Batch", back_populates="smtp_account")
