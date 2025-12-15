import time
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.auth.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from app.auth.db import SessionLocal
from app.auth.profile_db import ProfileDB
from app.auth.subscription_db import SubscriptionDB
from app.auth.user_db import UserDB

import jwt

SECRET_KEY = "supersecret"  # пример для учебного кейса

class AuthService:
    async def register(self, data: RegisterRequest) -> RegisterResponse:
        async with SessionLocal() as session:
            db_user = UserDB(
                email=data.email,
                password=data.password,
                full_name=data.full_name,
            )
            session.add(db_user)
            try:
                await session.commit()
                await session.refresh(db_user)
            except IntegrityError:
                raise ValueError("Пользователь с таким email уже существует")

            # Создаём профиль пользователя
            db_profile = ProfileDB(
                user_id=db_user.id,
                storage_used=0,
                storage_limit=2147483647  # лимит по ТЗ, можно заменить
            )
            session.add(db_profile)

            # Создаём дефолтную подписку
            subscription = SubscriptionDB(
                user_id=db_user.id,
                plan="basic",
                renewal_date=datetime.utcnow() + timedelta(days=30)
            )
            session.add(subscription)

            # Коммитим одну транзакцию с профилем и подпиской
            await session.commit()
            await session.refresh(db_profile)

            return RegisterResponse(
                id=str(db_user.id),
                email=db_user.email,
                full_name=db_user.full_name,
                created_at=db_user.created_at,
            )

    async def login(self, data: LoginRequest) -> LoginResponse:
        async with SessionLocal() as session:
            result = await session.execute(
                select(UserDB).where(
                    UserDB.email == data.email,
                    UserDB.password == data.password
                )
            )
            user = result.scalar_one_or_none()
            if user is None:
                raise ValueError("Неверный email или пароль")
            payload = {
                "sub": str(user.id),
                "email": user.email,
                "exp": int(time.time()) + 3600*24,
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return LoginResponse(access_token=token, expires_in=3600*24)
