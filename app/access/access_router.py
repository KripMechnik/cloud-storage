from fastapi import APIRouter, Depends, HTTPException
from app.access.access import AccessGrantRequest, AccessRevokeRequest
from app.access.access_service import AccessService
from app.access.dependencies import get_current_user

access_router = APIRouter(prefix="/api/access", tags=["Access"])

@access_router.post("/grant")
async def grant_access(data: AccessGrantRequest, _: str = Depends(get_current_user)):
    service = AccessService()
    try:
        await service.grant_access(data)
        return {"message": "Access granted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@access_router.post("/revoke")
async def revoke_access(data: AccessRevokeRequest, _: str = Depends(get_current_user)):
    service = AccessService()
    try:
        await service.revoke_access(data)
        return {"message": "Access revoked successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")