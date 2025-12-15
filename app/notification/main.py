# app/main.py
from fastapi import FastAPI

from app.notification.notification_router import notification_router

app = FastAPI()
app.include_router(notification_router)


