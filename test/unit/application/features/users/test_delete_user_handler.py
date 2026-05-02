from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from fastapi_example.application.exceptions.http_exceptions import (
    NotFoundError,
    ForbiddenError,
)
from fastapi_example.application.features.users.delete_user.handler import (
    DeleteUserHandler,
)
from fastapi_example.application.features.users.delete_user.command import (
    DeleteUserCommand,
)
from fastapi_example.application.interfaces.services import TEmailMessage
from fastapi_example.domain.entities import User


class TestDeleteUserHandler:
    @pytest.fixture
    def delete_user_handler(
        self,
        mock_users_repository,
        mock_hasher,
        mock_transaction_manager,
        mock_email_notifications,
    ) -> DeleteUserHandler:
        return DeleteUserHandler(
            repository=mock_users_repository,
            hasher=mock_hasher,
            transaction_manager=mock_transaction_manager,
            email_notifications=mock_email_notifications,
        )

    @pytest.mark.asyncio
    async def test_delete_user_success(
        self,
        delete_user_handler: DeleteUserHandler,
        mock_users_repository,
        mock_hasher,
        mock_email_notifications,
    ):
        user_id = uuid4()
        cmd = DeleteUserCommand(
            user_id=user_id,
            password="TestPassword123!",
        )

        user = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=user)
        mock_hasher.verify_password = MagicMock(return_value=True)
        mock_users_repository.delete_user = AsyncMock(return_value=user)

        result = await delete_user_handler.execute(cmd)

        assert result.id == user_id
        mock_users_repository.get_user.assert_called_once_with(
            user_id=user_id, for_update=True
        )
        mock_hasher.verify_password.assert_called_once_with(cmd.password, user.password)
        mock_users_repository.delete_user.assert_called_once_with(user_id=user_id)
        mock_email_notifications.enqueue.assert_called_once()
        enqueued: TEmailMessage = mock_email_notifications.enqueue.call_args.args[0]
        assert enqueued.recipient == user.email
        assert enqueued.subject == "Account deleted"

    @pytest.mark.asyncio
    async def test_delete_user_not_found(
        self,
        delete_user_handler: DeleteUserHandler,
        mock_users_repository,
        mock_email_notifications,
    ):
        user_id = uuid4()
        cmd = DeleteUserCommand(
            user_id=user_id,
            password="TestPassword123!",
        )

        mock_users_repository.get_user = AsyncMock(return_value=None)

        with pytest.raises(NotFoundError, match="User not found"):
            await delete_user_handler.execute(cmd)

        mock_email_notifications.enqueue.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_user_wrong_password(
        self,
        delete_user_handler: DeleteUserHandler,
        mock_users_repository,
        mock_hasher,
        mock_email_notifications,
    ):
        user_id = uuid4()
        cmd = DeleteUserCommand(
            user_id=user_id,
            password="WrongPassword123!",
        )

        user = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=user)
        mock_hasher.verify_password = MagicMock(return_value=False)

        with pytest.raises(ForbiddenError, match="Incorrect password confirmation"):
            await delete_user_handler.execute(cmd)

        mock_email_notifications.enqueue.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_user_verifies_password(
        self,
        delete_user_handler: DeleteUserHandler,
        mock_users_repository,
        mock_hasher,
        mock_email_notifications,
    ):
        user_id = uuid4()
        cmd = DeleteUserCommand(
            user_id=user_id,
            password="TestPassword123!",
        )

        user = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=user)
        mock_hasher.verify_password = MagicMock(return_value=True)
        mock_users_repository.delete_user = AsyncMock(return_value=user)

        await delete_user_handler.execute(cmd)

        mock_hasher.verify_password.assert_called_once_with(cmd.password, user.password)
        mock_email_notifications.enqueue.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_user_empty_password(
        self,
        delete_user_handler: DeleteUserHandler,
        mock_users_repository,
        mock_hasher,
        mock_email_notifications,
    ):
        user_id = uuid4()
        cmd = DeleteUserCommand(
            user_id=user_id,
            password="",
        )

        user = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=user)
        mock_hasher.verify_password = MagicMock(return_value=False)

        with pytest.raises(ForbiddenError):
            await delete_user_handler.execute(cmd)

        mock_email_notifications.enqueue.assert_not_called()
