# app/main.py
from fastapi import FastAPI

from app.audit.audit_log_router import audit_router

app = FastAPI()
app.include_router(audit_router)


