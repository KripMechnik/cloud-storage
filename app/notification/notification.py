# app/models/notification.py
from pydantic import BaseModel
from datetime import datetime

class NotificationItem(BaseModel):
    id: str
    title: str
    message: str
    created_at: datetime
    read: bool
