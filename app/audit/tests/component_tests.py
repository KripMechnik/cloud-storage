# test_audit_service.py
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock

import pytest
import pytest_asyncio
from sqlalchemy.exc import SQLAlchemyError

from app.audit.audit_log import AuditLogItem
from app.audit.audit_log_db import AuditLogDB
from app.audit.audit_log_service import AuditLogService


class TestAuditLogService:

    @pytest_asyncio.fixture
    async def audit_log_service(self):
        return AuditLogService()

    @pytest.fixture
    def sample_audit_logs(self):
        return [
            AuditLogDB(
                id="log_1",
                user_id="user_123",
                action="file_upload",
                details="Uploaded file.txt",
                timestamp=datetime(2024, 1, 15, 10, 30, 0)
            ),
            AuditLogDB(
                id="log_2",
                user_id="user_123",
                action="file_download",
                details="Downloaded file.pdf",
                timestamp=datetime(2024, 1, 15, 11, 0, 0)
            )
        ]

    @pytest.mark.asyncio
    async def test_get_logs_success(self, audit_log_service, sample_audit_logs):
        user_id = "user_123"
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=MagicMock(
            scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=sample_audit_logs)))))

        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__ = AsyncMock(return_value=mock_session)
        mock_context_manager.__aexit__ = AsyncMock(return_value=None)

        with patch('app.audit.audit_log_service.SessionLocal', return_value=mock_context_manager):
            result = await audit_log_service.get_logs(user_id)

        mock_session.execute.assert_awaited_once()
        assert result["total"] == 2
        assert len(result["logs"]) == 2
        assert isinstance(result["logs"][0], AuditLogItem)
        assert result["logs"][0].user_id == user_id

    @pytest.mark.asyncio
    async def test_get_logs_with_action_filter(self, audit_log_service, sample_audit_logs):
        user_id = "user_123"
        action = "file_upload"

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=MagicMock(
            scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[sample_audit_logs[0]])))))

        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__ = AsyncMock(return_value=mock_session)
        mock_context_manager.__aexit__ = AsyncMock(return_value=None)

        with patch('app.audit.audit_log_service.SessionLocal', return_value=mock_context_manager):
            result = await audit_log_service.get_logs(user_id, action=action)

        mock_session.execute.assert_awaited_once()
        assert result["total"] == 1
        assert result["logs"][0].action == action

    @pytest.mark.asyncio
    async def test_get_logs_with_date_filters(self, audit_log_service, sample_audit_logs):
        user_id = "user_123"
        date_from = "2024-01-15T10:00:00"
        date_to = "2024-01-15T11:00:00"

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=MagicMock(
            scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=sample_audit_logs)))))

        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__ = AsyncMock(return_value=mock_session)
        mock_context_manager.__aexit__ = AsyncMock(return_value=None)

        with patch('app.audit.audit_log_service.SessionLocal', return_value=mock_context_manager):
            result = await audit_log_service.get_logs(user_id, date_from=date_from, date_to=date_to)

        mock_session.execute.assert_awaited_once()
        assert result["total"] == 2

    @pytest.mark.asyncio
    async def test_get_logs_with_all_filters(self, audit_log_service, sample_audit_logs):
        user_id = "user_123"
        action = "file_upload"
        date_from = "2024-01-15T10:00:00"
        date_to = "2024-01-15T11:00:00"

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=MagicMock(
            scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[sample_audit_logs[0]])))))

        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__ = AsyncMock(return_value=mock_session)
        mock_context_manager.__aexit__ = AsyncMock(return_value=None)

        with patch('app.audit.audit_log_service.SessionLocal', return_value=mock_context_manager):
            result = await audit_log_service.get_logs(user_id, action=action, date_from=date_from, date_to=date_to)

        mock_session.execute.assert_awaited_once()
        assert result["total"] == 1
        assert result["logs"][0].action == action

    @pytest.mark.asyncio
    async def test_get_logs_empty_result(self, audit_log_service):
        user_id = "user_123"

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(
            return_value=MagicMock(scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[])))))

        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__ = AsyncMock(return_value=mock_session)
        mock_context_manager.__aexit__ = AsyncMock(return_value=None)

        with patch('app.audit.audit_log_service.SessionLocal', return_value=mock_context_manager):
            result = await audit_log_service.get_logs(user_id)

        mock_session.execute.assert_awaited_once()
        assert result["total"] == 0
        assert len(result["logs"]) == 0
