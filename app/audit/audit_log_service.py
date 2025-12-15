from sqlalchemy import select, and_
from datetime import datetime

from app.audit.audit_log import AuditLogItem
from app.audit.audit_log_db import AuditLogDB
from app.audit.db import SessionLocal


class AuditLogService:
    async def get_logs(self, user_id, action=None, date_from=None, date_to=None):
        async with SessionLocal() as session:
            filters = [AuditLogDB.user_id == user_id]
            if action:
                filters.append(AuditLogDB.action == action)
            if date_from:
                filters.append(AuditLogDB.timestamp >= datetime.fromisoformat(date_from))
            if date_to:
                filters.append(AuditLogDB.timestamp <= datetime.fromisoformat(date_to))

            stmt = select(AuditLogDB).where(and_(*filters)).order_by(AuditLogDB.timestamp.desc())
            result = await session.execute(stmt)
            logs = result.scalars().all()
            return {
                "logs": [
                    AuditLogItem(
                        **{**l.__dict__, "user_id": str(l.user_id)}
                    ) for l in logs
                ],
                "total": len(logs)
            }

