# app/services/access_service.py
from sqlalchemy import select

from app.access.access_db import AccessDB

from app.access.access import AccessGrantRequest, AccessRevokeRequest
from app.access.db import SessionLocal


class AccessService:
    async def grant_access(self, data: AccessGrantRequest):
        async with SessionLocal() as session:
            access = AccessDB(
                file_id=data.file_id,
                user_id=data.user_id,
                permission=data.permission
            )
            session.add(access)
            await session.commit()

    async def revoke_access(self, data: AccessRevokeRequest):
        async with SessionLocal() as session:
            result = await session.execute(
                select(AccessDB).where(
                    AccessDB.file_id == data.file_id,
                    AccessDB.user_id == data.user_id
                )
            )
            access = result.scalar_one_or_none()
            if access is None:
                raise ValueError("Доступ не найден")
            await session.delete(access)
            await session.commit()