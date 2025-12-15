# app/main.py
from fastapi import FastAPI

from app.config.config_router import config_router

app = FastAPI()
app.include_router(config_router)