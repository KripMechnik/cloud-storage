from fastapi import APIRouter, HTTPException

from app.auth.auth import LoginRequest, LoginResponse, BaseResponse
from app.auth.auth import RegisterRequest, RegisterResponse
from app.auth.auth_service import AuthService

auth_router = APIRouter(prefix="/docker-compose ps", tags=["Authentication"])


@auth_router.get("/", response_model=BaseResponse)
async def test():
    return BaseResponse(text="Hellow")


@auth_router.post("/register", response_model=RegisterResponse)
async def register_user(request: RegisterRequest):
    service = AuthService()
    try:
        return await service.register(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error: " + str(e))

@auth_router.post("/login", response_model=LoginResponse)
async def login_user(request: LoginRequest):
    service = AuthService()
    try:
        return await service.login(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error: " + str(e))