from sqlalchemy import Column, Integer, Text

from app.config.db import Base


class ConfigDB(Base):
    __tablename__ = "config"
    id = Column(Integer, primary_key=True)
    max_file_size = Column(Integer, nullable=False)
    allowed_file_types = Column(Text, nullable=False)  # JSON-строка, например: '["pdf","doc","jpg"]'
    storage_cleanup_days = Column(Integer, nullable=False)
