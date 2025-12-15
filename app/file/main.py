# app/main.py
from fastapi import FastAPI

from app.file.file_router import file_router

app = FastAPI()
app.include_router(file_router)


