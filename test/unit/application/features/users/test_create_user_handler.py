from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from fastapi_example.application.exceptions.http_exceptions import ConflictError
from fastapi_example.application.features.users.create_user.command import (
    CreateUserCommand,
)
from fastapi_example.application.features.users.create_user.handler import (
    CreateUserHandler,
)
from fastapi_example.domain.entities import User


class TestCreateUserHandler:
    @pytest.fixture
    def create_user_handler(
        self,
        mock_users_repository,
        mock_hasher,
        mock_transaction_manager,
    ) -> CreateUserHandler:
        return CreateUserHandler(
            repository=mock_users_repository,
            hasher=mock_hasher,
            transaction_manager=mock_transaction_manager,
        )

    @pytest.mark.asyncio
    async def test_create_user_success(
        self,
        create_user_handler: CreateUserHandler,
        mock_users_repository,
        mock_hasher,
    ):
        user_id = uuid4()
        cmd = CreateUserCommand(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
        )

        mock_users_repository.exists_user = AsyncMock(return_value=False)
        created_user = User(
            id=user_id,
            username=cmd.username,
            email=cmd.email,
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )
        mock_users_repository.create_user = AsyncMock(return_value=created_user)
        mock_hasher.hash_password = MagicMock(return_value="hashed_password")

        result = await create_user_handler.execute(cmd)

        assert result.username == cmd.username
        assert result.email == cmd.email
        mock_users_repository.create_user.assert_called_once()
        mock_hasher.hash_password.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_already_exists(
        self,
        create_user_handler: CreateUserHandler,
        mock_users_repository,
    ):
        cmd = CreateUserCommand(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
        )

        mock_users_repository.exists_user = AsyncMock(return_value=True)

        with pytest.raises(ConflictError):
            await create_user_handler.execute(cmd)

        mock_users_repository.create_user.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_user_hashes_password(
        self,
        create_user_handler: CreateUserHandler,
        mock_users_repository,
        mock_hasher,
    ):
        user_id = uuid4()
        cmd = CreateUserCommand(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
        )

        mock_users_repository.exists_user = AsyncMock(return_value=False)
        created_user = User(
            id=user_id,
            username=cmd.username,
            email=cmd.email,
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )
        mock_users_repository.create_user = AsyncMock(return_value=created_user)
        mock_hasher.hash_password = MagicMock(return_value="hashed_password")

        await create_user_handler.execute(cmd)

        mock_hasher.hash_password.assert_called_once_with("TestPassword123!")

    @pytest.mark.asyncio
    async def test_create_user_checks_username_and_email(
        self,
        create_user_handler: CreateUserHandler,
        mock_users_repository,
    ):
        cmd = CreateUserCommand(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
        )

        mock_users_repository.exists_user = AsyncMock(return_value=True)

        with pytest.raises(ConflictError):
            await create_user_handler.execute(cmd)

        mock_users_repository.exists_user.assert_called_once_with(
            username=cmd.username,
            email=cmd.email,
        )

    @pytest.mark.asyncio
    async def test_create_user_with_special_characters(
        self,
        create_user_handler: CreateUserHandler,
        mock_users_repository,
        mock_hasher,
    ):
        user_id = uuid4()
        cmd = CreateUserCommand(
            username="test.user-123",
            email="test.user+tag@example.com",
            password="P@ssw0rd!@#$",
        )

        mock_users_repository.exists_user = AsyncMock(return_value=False)
        created_user = User(
            id=user_id,
            username=cmd.username,
            email=cmd.email,
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )
        mock_users_repository.create_user = AsyncMock(return_value=created_user)
        mock_hasher.hash_password = MagicMock(return_value="hashed_password")

        result = await create_user_handler.execute(cmd)

        assert result.username == cmd.username
        assert result.email == cmd.email
