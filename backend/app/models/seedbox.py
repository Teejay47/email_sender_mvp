# backend/app/models/seedbox.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from .base import Base


class SeedBox(Base):
    __tablename__ = "seedboxes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    email_address = Column(String(320), nullable=False, index=True)
    last_status = Column(String(255), nullable=True)
    last_checked = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="seedboxes")
