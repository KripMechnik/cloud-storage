# app/models/subscription.py
from pydantic import BaseModel
from datetime import datetime

class SubscriptionResponse(BaseModel):
    plan: str
    storage_limit: int
    storage_used: int
    renewal_date: datetime

class SubscriptionUpgradeRequest(BaseModel):
    plan: str  # новый тарифный план ("basic", "premium", "business")

class SubscriptionUpgradeResponse(BaseModel):
    message: str
    new_plan: str
    storage_limit: int
