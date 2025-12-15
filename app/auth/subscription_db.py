# app/models/subscription_db.py
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.auth.db import Base


class SubscriptionDB(Base):
    __tablename__ = "subscriptions"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    plan = Column(String, nullable=False)  # например, "premium"
    renewal_date = Column(DateTime, nullable=False)
