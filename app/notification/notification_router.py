from fastapi import APIRouter, Depends, Query, HTTPException

from app.notification.dependencies import get_current_user
from app.notification.notification import NotificationItem
from app.notification.notification_service import NotificationService

notification_router = APIRouter(tags=["Notifications"])

@notification_router.get("/api/notifications", response_model=list[NotificationItem])
async def get_notifications(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    user_id: str = Depends(get_current_user)
):
    service = NotificationService()
    return await service.get_notifications(user_id, page, limit)

@notification_router.post("/api/notifications/{id}/read")
async def mark_notification_as_read(
    id: str,
    user_id: str = Depends(get_current_user)
):
    service = NotificationService()
    try:
        return await service.mark_as_read(user_id, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
