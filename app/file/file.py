# app/models/file.py
from pydantic import BaseModel
from datetime import datetime

class FileUploadResponse(BaseModel):
    id: str
    name: str
    size: int
    uploaded_at: datetime

class FileDownloadResponse(BaseModel):
    name: str
