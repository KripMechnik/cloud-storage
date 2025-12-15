import json

from sqlalchemy import select

from app.config.config_db import ConfigDB
from app.config.db import SessionLocal


class ConfigService:
    async def get_config(self):
        async with SessionLocal() as session:
            config = await session.execute(select(ConfigDB))
            config = config.scalar_one_or_none()
            if not config:
                raise ValueError("Config not found")
            return {
                "max_file_size": config.max_file_size,
                "allowed_file_types": json.loads(config.allowed_file_types),
                "storage_cleanup_days": config.storage_cleanup_days
            }

    async def set_config(self, key: str, value):
        async with SessionLocal() as session:
            config = await session.execute(select(ConfigDB))
            config = config.scalar_one_or_none()
            if not config:
                raise ValueError("Config not found")
            # сериализация для массива
            if key == "allowed_file_types" and isinstance(value, list):
                value = json.dumps(value)
            setattr(config, key, value)
            await session.commit()
            return {"message": "Config updated successfully"}