from fastapi import APIRouter, HTTPException

from app.profile.dependencies import get_current_user
from app.profile.profile import ProfileResponse, ProfileUpdateRequest
from app.profile.profile_service import ProfileService
from fastapi import Depends

profile_router = APIRouter(prefix="/api", tags=["Profile"])


@profile_router.get("/profile", response_model=ProfileResponse)
async def get_profile(user_id: str = Depends(get_current_user)):
    service = ProfileService()
    try:
        return await service.get_profile(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Неверный формат user_id")

@profile_router.put("/profile")
async def update_profile(
    data: ProfileUpdateRequest,
    user_id: str = Depends(get_current_user)
):
    service = ProfileService()
    try:
        await service.update_profile(user_id, data)
        return {"message": "Profile updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
