# app/main.py
from fastapi import FastAPI

from app.subscription.subscription_router import subscription_router

app = FastAPI()
app.include_router(subscription_router)


