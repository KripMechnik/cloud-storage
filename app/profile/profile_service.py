# app/services/profile_service.py
from sqlalchemy import update
from sqlalchemy.future import select

from app.profile.db import SessionLocal
from app.profile.profile import ProfileResponse, ProfileUpdateRequest
from app.profile.profile_db import ProfileDB
from app.profile.user_db import UserDB


class ProfileService:
    async def get_profile(self, user_id: str) -> ProfileResponse:
        async with SessionLocal() as session:
            user_result = await session.execute(select(UserDB).where(UserDB.id == user_id))
            user = user_result.scalar_one_or_none()
            profile_result = await session.execute(select(ProfileDB).where(ProfileDB.user_id == user_id))
            profile = profile_result.scalar_one_or_none()
            if not user or not profile:
                raise ValueError("Профиль или пользователь не найден")
            return ProfileResponse(
                id=str(user.id),
                email=user.email,
                full_name=user.full_name,
                storage_used=profile.storage_used,
                storage_limit=profile.storage_limit,
                created_at=user.created_at,
            )

    async def update_profile(self, user_id: str, data: ProfileUpdateRequest):
        async with SessionLocal() as session:
            # Обновляем поле full_name в UserDB (основная таблица пользователей)
            result = await session.execute(
                update(UserDB)
                .where(UserDB.id == user_id)
                .values(full_name=data.full_name)
            )
            if result.rowcount == 0:
                raise ValueError("Пользователь не найден")
            await session.commit()

