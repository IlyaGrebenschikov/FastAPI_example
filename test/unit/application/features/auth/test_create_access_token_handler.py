from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from fastapi_example.application.exceptions.http_exceptions import UnAuthorizedError
from fastapi_example.application.features.auth.create_access_token.command import (
    CreateAccessTokenCommand,
)
from fastapi_example.application.features.auth.create_access_token.handler import (
    CreateAccessTokenHandler,
)
from fastapi_example.application.services.token_jwt import TokenJWTService
from fastapi_example.domain.entities import User


class TestCreateAccessTokenHandler:
    @pytest.fixture
    def create_access_token_handler(
        self,
        mock_users_repository,
        mock_hasher,
        mock_transaction_manager,
        jwt_settings,
    ) -> CreateAccessTokenHandler:
        token_service = TokenJWTService(jwt_settings)
        return CreateAccessTokenHandler(
            user_repository=mock_users_repository,
            token_jwt=token_service,
            hasher=mock_hasher,
            transaction_manager=mock_transaction_manager,
        )

    @pytest.mark.asyncio
    async def test_create_access_token_success(
        self,
        create_access_token_handler: CreateAccessTokenHandler,
        mock_users_repository,
        mock_hasher,
    ):
        user_id = uuid4()
        cmd = CreateAccessTokenCommand(
            username="testuser",
            password="TestPassword123!",
        )

        user = User(
            id=user_id,
            username=cmd.username,
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=user)
        mock_hasher.verify_password = MagicMock(return_value=True)

        token = await create_access_token_handler.execute(cmd)

        assert isinstance(token, str)
        assert len(token) > 0
        mock_users_repository.get_user.assert_called_once_with(username=cmd.username)
        mock_hasher.verify_password.assert_called_once_with(
            cmd.password, user.password
        )

    @pytest.mark.asyncio
    async def test_create_access_token_user_not_found(
        self,
        create_access_token_handler: CreateAccessTokenHandler,
        mock_users_repository,
    ):
        cmd = CreateAccessTokenCommand(
            username="nonexistent",
            password="TestPassword123!",
        )

        mock_users_repository.get_user = AsyncMock(return_value=None)

        with pytest.raises(UnAuthorizedError, match="Incorrect login or password"):
            await create_access_token_handler.execute(cmd)

    @pytest.mark.asyncio
    async def test_create_access_token_wrong_password(
        self,
        create_access_token_handler: CreateAccessTokenHandler,
        mock_users_repository,
        mock_hasher,
    ):
        user_id = uuid4()
        cmd = CreateAccessTokenCommand(
            username="testuser",
            password="WrongPassword123!",
        )

        user = User(
            id=user_id,
            username=cmd.username,
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=user)
        mock_hasher.verify_password = MagicMock(return_value=False)

        with pytest.raises(UnAuthorizedError, match="Incorrect login or password"):
            await create_access_token_handler.execute(cmd)

    @pytest.mark.asyncio
    async def test_create_access_token_with_scopes(
        self,
        create_access_token_handler: CreateAccessTokenHandler,
        mock_users_repository,
        mock_hasher,
    ):
        user_id = uuid4()
        cmd = CreateAccessTokenCommand(
            username="testuser",
            password="TestPassword123!",
            scopes=["read", "write"],
        )

        user = User(
            id=user_id,
            username=cmd.username,
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=user)
        mock_hasher.verify_password = MagicMock(return_value=True)

        token = await create_access_token_handler.execute(cmd)

        assert isinstance(token, str)
        assert len(token) > 0

    @pytest.mark.asyncio
    async def test_create_access_token_verifies_password(
        self,
        create_access_token_handler: CreateAccessTokenHandler,
        mock_users_repository,
        mock_hasher,
    ):
        user_id = uuid4()
        cmd = CreateAccessTokenCommand(
            username="testuser",
            password="TestPassword123!",
        )

        user = User(
            id=user_id,
            username=cmd.username,
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=user)
        mock_hasher.verify_password = MagicMock(return_value=True)

        await create_access_token_handler.execute(cmd)

        mock_hasher.verify_password.assert_called_once_with(
            cmd.password, user.password
        )

    @pytest.mark.asyncio
    async def test_create_access_token_empty_username(
        self,
        create_access_token_handler: CreateAccessTokenHandler,
        mock_users_repository,
    ):
        cmd = CreateAccessTokenCommand(
            username="",
            password="TestPassword123!",
        )

        mock_users_repository.get_user = AsyncMock(return_value=None)

        with pytest.raises(UnAuthorizedError):
            await create_access_token_handler.execute(cmd)
