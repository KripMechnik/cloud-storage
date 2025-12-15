from fastapi import APIRouter, Depends, Query
from app.audit.audit_log_service import AuditLogService
from app.audit.dependencies import get_current_user

audit_router = APIRouter(tags=["Logs"])

@audit_router.get("/api/audit/logs")
async def get_logs(
    action: str = Query(None),
    date_from: str = Query(None),
    date_to: str = Query(None),
    user_id: str = Depends(get_current_user)
):
    service = AuditLogService()
    return await service.get_logs(user_id, action, date_from, date_to)
