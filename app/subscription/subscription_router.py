# app/endpoints/subscription_router.py
from fastapi import APIRouter, Depends, HTTPException

from app.subscription.dependencies import get_current_user
from app.subscription.subscription import SubscriptionResponse, SubscriptionUpgradeRequest
from app.subscription.subscription_service import SubscriptionService

subscription_router = APIRouter(tags=["Subscription"])
@subscription_router.get("/api/subscription")

@subscription_router.get("/api/subscription", response_model=SubscriptionResponse)
async def get_subscription(user_id: str = Depends(get_current_user)):
    service = SubscriptionService()
    try:
        return await service.get_subscription(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@subscription_router.post("/api/subscription/upgrade")
async def upgrade_subscription(
    data: SubscriptionUpgradeRequest,
    user_id: str = Depends(get_current_user)
):
    service = SubscriptionService()
    try:
        return await service.upgrade_subscription(user_id, data.plan)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")