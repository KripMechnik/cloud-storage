from pydantic import BaseModel
from datetime import datetime

class AuditLogItem(BaseModel):
    id: str
    user_id: str
    action: str
    details: str
    timestamp: datetime

class AuditLogResponse(BaseModel):
    logs: list[AuditLogItem]
    total: int
