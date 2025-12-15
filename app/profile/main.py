# app/main.py
from fastapi import FastAPI

from app.profile.profile_router import profile_router

app = FastAPI()
app.include_router(profile_router)


