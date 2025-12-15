# test_auth_service.py
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

import jwt
import pytest

from app.auth.auth import RegisterRequest, LoginRequest


class TestAuthRouter:
    @pytest.fixture
    def register_request_data(self):
        return RegisterRequest(
            email="test@example.com",
            password="password123",
            full_name="Test User"
        )

    @pytest.fixture
    def login_request_data(self):
        return LoginRequest(
            email="test@example.com",
            password="password123"
        )

    @pytest.fixture
    def mock_register_response(self):
        from app.auth.auth import RegisterResponse
        return RegisterResponse(
            id="123e4567-e89b-12d3-a456-426614174000",
            email="test@example.com",
            full_name="Test User",
            created_at=datetime.utcnow()
        )

    @pytest.fixture
    def mock_login_response(self):
        from app.auth.auth import LoginResponse
        return LoginResponse(
            access_token="test_token",
            expires_in=86400
        )

    @pytest.mark.asyncio
    async def test_register_endpoint_success(self, register_request_data, mock_register_response):
        from app.auth.auth_router import register_user
        mock_service = AsyncMock()
        mock_service.register = AsyncMock(return_value=mock_register_response)

        # Act
        with patch('app.auth.auth_router.AuthService', return_value=mock_service):
            result = await register_user(register_request_data)

        # Assert
        mock_service.register.assert_awaited_once_with(register_request_data)
        assert result == mock_register_response

    @pytest.mark.asyncio
    async def test_register_endpoint_duplicate_email(self, register_request_data):
        from app.auth.auth_router import register_user
        from fastapi import HTTPException

        mock_service = AsyncMock()
        mock_service.register = AsyncMock(side_effect=ValueError("Пользователь с таким email уже существует"))

        with patch('app.auth.auth_router.AuthService', return_value=mock_service):
            with pytest.raises(HTTPException) as exc_info:
                await register_user(register_request_data)

            assert exc_info.value.status_code == 400
            assert "Пользователь с таким email уже существует" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_register_endpoint_internal_error(self, register_request_data):
        from app.auth.auth_router import register_user
        from fastapi import HTTPException

        mock_service = AsyncMock()
        mock_service.register = AsyncMock(side_effect=Exception("Unexpected error"))

        with patch('app.auth.auth_router.AuthService', return_value=mock_service):
            with pytest.raises(HTTPException) as exc_info:
                await register_user(register_request_data)

            assert exc_info.value.status_code == 500
            assert "Internal Server Error" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_login_endpoint_success(self, login_request_data, mock_login_response):
        from app.auth.auth_router import login_user
        mock_service = AsyncMock()
        mock_service.login = AsyncMock(return_value=mock_login_response)

        with patch('app.auth.auth_router.AuthService', return_value=mock_service):
            result = await login_user(login_request_data)

        mock_service.login.assert_awaited_once_with(login_request_data)
        assert result == mock_login_response

    @pytest.mark.asyncio
    async def test_login_endpoint_invalid_credentials(self, login_request_data):
        from app.auth.auth_router import login_user
        from fastapi import HTTPException

        mock_service = AsyncMock()
        mock_service.login = AsyncMock(side_effect=ValueError("Неверный email или пароль"))

        with patch('app.auth.auth_router.AuthService', return_value=mock_service):
            with pytest.raises(HTTPException) as exc_info:
                await login_user(login_request_data)

            assert exc_info.value.status_code == 401
            assert "Неверный email или пароль" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_login_endpoint_internal_error(self, login_request_data):
        from app.auth.auth_router import login_user
        from fastapi import HTTPException

        mock_service = AsyncMock()
        mock_service.login = AsyncMock(side_effect=Exception("Unexpected error"))

        with patch('app.auth.auth_router.AuthService', return_value=mock_service):
            with pytest.raises(HTTPException) as exc_info:
                await login_user(login_request_data)

            assert exc_info.value.status_code == 500
            assert "Internal Server Error" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_test_endpoint(self):
        from app.auth.auth_router import test
        from app.auth.auth import BaseResponse

        result = await test()

        assert isinstance(result, BaseResponse)
        assert result.text == "Hellow"


class TestDependencies:
    def test_get_current_user_valid_token(self):
        from app.auth.dependencies import get_current_user
        from fastapi.security import HTTPAuthorizationCredentials

        test_user_id = "123e4567-e89b-12d3-a456-426614174000"
        valid_token = jwt.encode(
            {"sub": test_user_id, "exp": datetime.utcnow() + timedelta(hours=1)},
            "supersecret",
            algorithm="HS256"
        )

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=valid_token
        )

        with patch('app.auth.dependencies.jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": test_user_id}
            user_id = get_current_user(credentials)

        assert user_id == test_user_id

    def test_get_current_user_invalid_token(self):
        from app.auth.dependencies import get_current_user
        from fastapi.security import HTTPAuthorizationCredentials
        from fastapi import HTTPException

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid_token"
        )

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials)

        assert exc_info.value.status_code == 401
        assert "Invalid credentials" in str(exc_info.value.detail)

    def test_get_current_user_missing_sub(self):
        from app.auth.dependencies import get_current_user
        from fastapi.security import HTTPAuthorizationCredentials
        from fastapi import HTTPException

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="test_token"
        )

        with patch('app.auth.dependencies.jwt.decode') as mock_decode:
            mock_decode.return_value = {"email": "test@example.com"}  # нет sub
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(credentials)

            assert exc_info.value.status_code == 401
            assert "Invalid token" in str(exc_info.value.detail)