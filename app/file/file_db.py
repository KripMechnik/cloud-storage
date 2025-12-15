# app/models/file_db.py
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.file.db import Base


class FileDB(Base):
    __tablename__ = "files"
    id = Column(String, primary_key=True, default=lambda: "file-" + str(uuid.uuid4()))
    name = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    parent_id = Column(String, nullable=True)
