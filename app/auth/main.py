# app/main.py
from fastapi import FastAPI

from app.auth.auth_router import auth_router

app = FastAPI()
app.include_router(auth_router)

