# app/services/subscription_service.py
from sqlalchemy import select

from app.subscription.db import SessionLocal
from app.subscription.profile_db import ProfileDB
from app.subscription.subscription import SubscriptionResponse
from app.subscription.subscription_db import SubscriptionDB


PLAN_LIMITS = {
    "basic": 10_000,      # 10 Кб
    "premium": 50_000,    # 50 Кб
    "business": 100_000,  # 100 Кб
}

class SubscriptionService:
    async def get_subscription(self, user_id: str):
        async with SessionLocal() as session:
            subscription = await session.get(SubscriptionDB, user_id)
            if not subscription:
                raise ValueError("Подписка не найдена")

            stmt = select(ProfileDB).where(ProfileDB.user_id == user_id)
            result = await session.execute(stmt)
            profile = result.scalar_one_or_none()
            if not profile:
                raise ValueError("Профиль не найден")

            return SubscriptionResponse(
                plan=subscription.plan,
                storage_limit=profile.storage_limit,
                storage_used=profile.storage_used,
                renewal_date=subscription.renewal_date,
            )

    async def upgrade_subscription(self, user_id: str, plan: str):
        try:
            async with SessionLocal() as session:
                subscription: SubscriptionDB = await session.get(SubscriptionDB, user_id)
                if not subscription:
                    raise ValueError("Подписка не найдена")
                subscription.plan = plan

                stmt = select(ProfileDB).where(ProfileDB.user_id == user_id)
                result = await session.execute(stmt)
                profile = result.scalar_one_or_none()
                if not profile:
                    raise ValueError("Профиль не найден")
                new_limit = PLAN_LIMITS.get(plan, PLAN_LIMITS["basic"])
                profile.storage_limit = new_limit

                await session.commit()
                return {
                    "message": "Subscription upgraded successfully",
                    "new_plan": plan,
                    "storage_limit": new_limit,
                }
        except Exception as e:
            print(f"Ошибка: {e}")
            raise