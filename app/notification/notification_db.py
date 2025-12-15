# app/models/notification_db.py
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.notification.db import Base


class NotificationDB(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True)  # например, строковый идентификатор
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    read = Column(Boolean, default=False)
