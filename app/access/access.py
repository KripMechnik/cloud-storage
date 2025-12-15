# app/models/access.py
from pydantic import BaseModel

class AccessGrantRequest(BaseModel):
    file_id: str
    user_id: str
    permission: str  # 'read' или 'write'

class AccessRevokeRequest(BaseModel):
    file_id: str
    user_id: str
