from pydantic import BaseModel
from datetime import datetime

class ProfileResponse(BaseModel):
    id: str
    email: str
    full_name: str
    storage_used: int
    storage_limit: int
    created_at: datetime

class ProfileUpdateRequest(BaseModel):
    full_name: str
