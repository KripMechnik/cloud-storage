from sqlalchemy import select

from app.notification.db import SessionLocal
from app.notification.notification import NotificationItem
from app.notification.notification_db import NotificationDB


class NotificationService:
    async def get_notifications(self, user_id: str, page: int = 1, limit: int = 10):
        offset = (page - 1) * limit
        async with SessionLocal() as session:
            stmt = (
                select(NotificationDB)
                .where(NotificationDB.user_id == user_id)
                .order_by(NotificationDB.created_at.desc())
                .offset(offset)
                .limit(limit)
            )
            result = await session.execute(stmt)
            notifications = result.scalars().all()
            return [NotificationItem(**n.__dict__) for n in notifications]

    async def mark_as_read(self, user_id: str, notif_id: str):
        async with SessionLocal() as session:
            stmt = select(NotificationDB).where(
                NotificationDB.id == notif_id,
                NotificationDB.user_id == user_id
            )
            result = await session.execute(stmt)
            notif = result.scalar_one_or_none()
            if not notif:
                raise ValueError("Уведомление не найдено")
            notif.read = True
            await session.commit()
            return {"message": "Notification marked as read"}
