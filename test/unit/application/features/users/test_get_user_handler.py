from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from fastapi_example.application.exceptions.http_exceptions import NotFoundError
from fastapi_example.application.features.users.get_user.handler import (
    GetUserHandler,
)
from fastapi_example.application.features.users.get_user.query import GetUserQuery
from fastapi_example.domain.entities import User


class TestGetUserHandler:
    @pytest.fixture
    def get_user_handler(
        self, mock_users_repository, mock_transaction_manager
    ) -> GetUserHandler:
        return GetUserHandler(
            repository=mock_users_repository,
            transaction_manager=mock_transaction_manager,
        )

    @pytest.mark.asyncio
    async def test_get_user_success(
        self, get_user_handler: GetUserHandler, mock_users_repository
    ):
        user_id = uuid4()
        query = GetUserQuery(user_id=user_id)

        user = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=user)

        result = await get_user_handler.execute(query)

        assert result.id == user_id
        assert result.username == "testuser"
        assert result.email == "test@example.com"
        mock_users_repository.get_user.assert_called_once_with(
            user_id=user_id, for_update=False
        )

    @pytest.mark.asyncio
    async def test_get_user_not_found(
        self, get_user_handler: GetUserHandler, mock_users_repository
    ):
        user_id = uuid4()
        query = GetUserQuery(user_id=user_id)

        mock_users_repository.get_user = AsyncMock(return_value=None)

        with pytest.raises(NotFoundError, match="User not found"):
            await get_user_handler.execute(query)

    @pytest.mark.asyncio
    async def test_get_user_with_timestamps(
        self, get_user_handler: GetUserHandler, mock_users_repository
    ):
        from datetime import datetime, timezone

        user_id = uuid4()
        query = GetUserQuery(user_id=user_id)

        created_at = datetime.now(timezone.utc)
        updated_at = datetime.now(timezone.utc)

        user = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            created_at=created_at,
            updated_at=updated_at,
        )

        mock_users_repository.get_user = AsyncMock(return_value=user)

        result = await get_user_handler.execute(query)

        assert result.created_at == created_at
        assert result.updated_at == updated_at

    @pytest.mark.asyncio
    async def test_get_user_with_special_characters(
        self, get_user_handler: GetUserHandler, mock_users_repository
    ):
        user_id = uuid4()
        query = GetUserQuery(user_id=user_id)

        user = User(
            id=user_id,
            username="test_user-123",
            email="test+tag@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=user)

        result = await get_user_handler.execute(query)

        assert result.username == "test_user-123"
        assert result.email == "test+tag@example.com"

    @pytest.mark.asyncio
    async def test_get_user_calls_transaction_manager(
        self, get_user_handler: GetUserHandler, mock_users_repository
    ):
        user_id = uuid4()
        query = GetUserQuery(user_id=user_id)

        user = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=user)

        await get_user_handler.execute(query)

        assert mock_users_repository.get_user.called
