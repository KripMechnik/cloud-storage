# app/main.py
from fastapi import FastAPI

from app.access.access_router import access_router

app = FastAPI()
app.include_router(access_router)


