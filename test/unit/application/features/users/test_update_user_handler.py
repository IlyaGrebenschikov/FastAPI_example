from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from fastapi_example.application.exceptions.http_exceptions import (
    NotFoundError,
    ConflictError,
)
from fastapi_example.application.interfaces.services import TEmailMessage
from fastapi_example.application.features.users.services import EmailValidatorService
from fastapi_example.application.features.users.update_user.handler import (
    UpdateUserHandler,
)
from fastapi_example.application.features.users.update_user.command import (
    UpdateUserCommand,
)
from fastapi_example.domain.entities import User


class TestUpdateUserHandler:
    @pytest.fixture
    def update_user_handler(
        self,
        mock_users_repository,
        mock_transaction_manager,
        mock_email_verifier,
        mock_email_notifications,
    ) -> UpdateUserHandler:
        return UpdateUserHandler(
            repository=mock_users_repository,
            transaction_manager=mock_transaction_manager,
            email_validator=EmailValidatorService(mock_email_verifier),
            email_notifications=mock_email_notifications,
        )

    @pytest.mark.asyncio
    async def test_update_user_success(
        self,
        update_user_handler: UpdateUserHandler,
        mock_users_repository,
        mock_email_notifications,
    ):
        user_id = uuid4()
        cmd = UpdateUserCommand(
            user_id=user_id,
            username="newusername",
            email="newemail@example.com",
        )

        existing_user = User(
            id=user_id,
            username="oldusername",
            email="oldemail@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        updated_user = User(
            id=user_id,
            username="newusername",
            email="newemail@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=existing_user)
        mock_users_repository.exists_user = AsyncMock(return_value=False)
        mock_users_repository.update_user = AsyncMock(return_value=updated_user)

        result = await update_user_handler.execute(cmd)

        assert result.username == "newusername"
        assert result.email == "newemail@example.com"
        mock_users_repository.get_user.assert_called_once_with(
            user_id=user_id, for_update=True
        )
        mock_users_repository.update_user.assert_called_once()
        mock_email_notifications.enqueue.assert_called_once()
        enqueued: TEmailMessage = mock_email_notifications.enqueue.call_args.args[0]
        assert enqueued.recipient == "newemail@example.com"
        assert enqueued.subject == "Account updated"

    @pytest.mark.asyncio
    async def test_update_user_not_found(
        self,
        update_user_handler: UpdateUserHandler,
        mock_users_repository,
        mock_email_notifications,
    ):
        user_id = uuid4()
        cmd = UpdateUserCommand(
            user_id=user_id,
            username="newusername",
        )

        mock_users_repository.get_user = AsyncMock(return_value=None)

        with pytest.raises(NotFoundError, match="User not found"):
            await update_user_handler.execute(cmd)

        mock_email_notifications.enqueue.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_user_username_already_exists(
        self,
        update_user_handler: UpdateUserHandler,
        mock_users_repository,
        mock_email_notifications,
    ):
        user_id = uuid4()
        cmd = UpdateUserCommand(
            user_id=user_id,
            username="existingusername",
        )

        existing_user = User(
            id=user_id,
            username="oldusername",
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=existing_user)
        mock_users_repository.exists_user = AsyncMock(return_value=True)

        with pytest.raises(ConflictError, match="User already exists with username"):
            await update_user_handler.execute(cmd)

        mock_email_notifications.enqueue.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_user_email_already_exists(
        self,
        update_user_handler: UpdateUserHandler,
        mock_users_repository,
        mock_email_notifications,
    ):
        user_id = uuid4()
        cmd = UpdateUserCommand(
            user_id=user_id,
            email="existingemail@example.com",
        )

        existing_user = User(
            id=user_id,
            username="testuser",
            email="oldemail@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=existing_user)
        mock_users_repository.exists_user = AsyncMock(return_value=True)

        with pytest.raises(ConflictError, match="User already exists with email"):
            await update_user_handler.execute(cmd)

        mock_email_notifications.enqueue.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_user_partial(
        self,
        update_user_handler: UpdateUserHandler,
        mock_users_repository,
        mock_email_notifications,
    ):
        user_id = uuid4()
        cmd = UpdateUserCommand(
            user_id=user_id,
            username="newusername",
            email=None,
        )

        existing_user = User(
            id=user_id,
            username="oldusername",
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        updated_user = User(
            id=user_id,
            username="newusername",
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=existing_user)
        mock_users_repository.exists_user = AsyncMock(return_value=False)
        mock_users_repository.update_user = AsyncMock(return_value=updated_user)

        result = await update_user_handler.execute(cmd)

        assert result.username == "newusername"
        assert result.email == "test@example.com"
        mock_email_notifications.enqueue.assert_called_once()
        enqueued: TEmailMessage = mock_email_notifications.enqueue.call_args.args[0]
        assert enqueued.recipient == "test@example.com"

    @pytest.mark.asyncio
    async def test_update_user_same_username(
        self,
        update_user_handler: UpdateUserHandler,
        mock_users_repository,
        mock_email_notifications,
    ):
        user_id = uuid4()
        cmd = UpdateUserCommand(
            user_id=user_id,
            username="sameusername",
        )

        existing_user = User(
            id=user_id,
            username="sameusername",
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        updated_user = User(
            id=user_id,
            username="sameusername",
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_users_repository.get_user = AsyncMock(return_value=existing_user)
        mock_users_repository.update_user = AsyncMock(return_value=updated_user)

        result = await update_user_handler.execute(cmd)

        assert result.username == "sameusername"
        mock_users_repository.exists_user.assert_not_called()
        mock_email_notifications.enqueue.assert_called_once()
