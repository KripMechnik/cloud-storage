# test_access_service.py
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from app.access.access import AccessGrantRequest, AccessRevokeRequest


class TestAccessRouter:

    @pytest.fixture
    def mock_current_user(self):
        return "test_user_123"

    @pytest.fixture
    def grant_request_data(self):
        return AccessGrantRequest(
            file_id="file_123",
            user_id="user_456",
            permission="write"
        )

    @pytest.fixture
    def revoke_request_data(self):
        return AccessRevokeRequest(
            file_id="file_123",
            user_id="user_456"
        )

    @pytest.mark.asyncio
    async def test_grant_access_endpoint_success(self, mock_current_user, grant_request_data):
        from app.access.access_router import grant_access
        mock_service = AsyncMock()

        with patch('app.access.access_router.AccessService', return_value=mock_service):
            result = await grant_access(grant_request_data, mock_current_user)

        mock_service.grant_access.assert_awaited_once_with(grant_request_data)
        assert result == {"message": "Access granted successfully"}

    @pytest.mark.asyncio
    async def test_grant_access_endpoint_error(self, mock_current_user, grant_request_data):
        from app.access.access_router import grant_access
        mock_service = AsyncMock()
        mock_service.grant_access = AsyncMock(side_effect=Exception("Test error"))

        with patch('app.access.access_router.AccessService', return_value=mock_service):
            with pytest.raises(HTTPException) as exc_info:
                await grant_access(grant_request_data, mock_current_user)

            assert exc_info.value.status_code == 500
            assert exc_info.value.detail == "Internal Server Error"

    @pytest.mark.asyncio
    async def test_revoke_access_endpoint_success(self, mock_current_user, revoke_request_data):
        from app.access.access_router import revoke_access
        mock_service = AsyncMock()

        with patch('app.access.access_router.AccessService', return_value=mock_service):
            result = await revoke_access(revoke_request_data, mock_current_user)

        mock_service.revoke_access.assert_awaited_once_with(revoke_request_data)
        assert result == {"message": "Access revoked successfully"}

    @pytest.mark.asyncio
    async def test_revoke_access_endpoint_not_found(self, mock_current_user, revoke_request_data):
        from app.access.access_router import revoke_access
        mock_service = AsyncMock()
        mock_service.revoke_access = AsyncMock(side_effect=ValueError("Доступ не найден"))

        with patch('app.access.access_router.AccessService', return_value=mock_service):
            with pytest.raises(HTTPException) as exc_info:
                await revoke_access(revoke_request_data, mock_current_user)

            assert exc_info.value.status_code == 404
            assert exc_info.value.detail == "Доступ не найден"