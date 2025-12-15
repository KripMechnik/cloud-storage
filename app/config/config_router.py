from fastapi import APIRouter, HTTPException

from app.config.config import ConfigSetResponse, ConfigSetRequest
from app.config.config_service import ConfigService

config_router = APIRouter(prefix="/api/config/get", tags=["Config"])

@config_router.get("")
async def get_config():
    service = ConfigService()
    try:
        return await service.get_config()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@config_router.put("/set", response_model=ConfigSetResponse)
async def set_config(
    req: ConfigSetRequest
):
    service = ConfigService()
    try:
        return await service.set_config(req.key, req.value)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))