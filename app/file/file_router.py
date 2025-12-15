# app/endpoints/file_router.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends

from app.file.dependencies import get_current_user
from app.file.file_service import FileService
from app.file.file import FileUploadResponse, FileDownloadResponse

file_router = APIRouter(prefix="/api/files", tags=["Files"])

@file_router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
    parent_id: str = Form(None)
):
    service = FileService()
    try:
        return await service.upload_file(file, user_id, parent_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@file_router.get("/{id}/download", response_model=FileDownloadResponse)
async def download_file(id: str):
    service = FileService()
    try:
        return await service.get_file_name(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@file_router.delete("/{id}")
async def delete_file(id: str, user_id: str = Depends(get_current_user)):
    service = FileService()
    try:
        await service.delete_file(id)
        return {"message": "File deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")