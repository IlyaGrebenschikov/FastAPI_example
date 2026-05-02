from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from fastapi_example.application.exceptions.http_exceptions import (
    ConflictError,
    BadRequestError,
    ServiceUnavailableError,
)
from fastapi_example.application.interfaces.http_clients import EmailVerificationResult
from fastapi_example.application.interfaces.services import TEmailMessage
from fastapi_example.application.features.users.services import EmailValidatorService
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
        mock_email_verifier,
        mock_email_notifications,
    ) -> CreateUserHandler:
        return CreateUserHandler(
            repository=mock_users_repository,
            hasher=mock_hasher,
            transaction_manager=mock_transaction_manager,
            email_validator=EmailValidatorService(mock_email_verifier),
            email_notifications=mock_email_notifications,
        )

    @pytest.mark.asyncio
    async def test_create_user_success(
        self,
        create_user_handler: CreateUserHandler,
        mock_users_repository,
        mock_hasher,
        mock_email_notifications,
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
        mock_email_notifications.enqueue.assert_called_once()
        enqueued: TEmailMessage = mock_email_notifications.enqueue.call_args.args[0]
        assert enqueued.recipient == cmd.email
        assert enqueued.subject == "Account created"

    @pytest.mark.asyncio
    async def test_create_user_already_exists(
        self,
        create_user_handler: CreateUserHandler,
        mock_users_repository,
        mock_email_notifications,
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
        mock_email_notifications.enqueue.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_user_hashes_password(
        self,
        create_user_handler: CreateUserHandler,
        mock_users_repository,
        mock_hasher,
        mock_email_notifications,
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
        mock_email_notifications.enqueue.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_checks_username_and_email(
        self,
        create_user_handler: CreateUserHandler,
        mock_users_repository,
        mock_email_notifications,
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
        mock_email_notifications.enqueue.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_user_with_special_characters(
        self,
        create_user_handler: CreateUserHandler,
        mock_users_repository,
        mock_hasher,
        mock_email_notifications,
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
        mock_email_notifications.enqueue.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_invalid_email_format(
        self,
        create_user_handler: CreateUserHandler,
        mock_email_verifier,
        mock_email_notifications,
    ):
        cmd = CreateUserCommand(
            username="testuser",
            email="invalid-email",
            password="TestPassword123!",
        )

        mock_email_verifier.check = AsyncMock(
            return_value=EmailVerificationResult(
                is_valid_format=False,
                is_deliverable=False,
                is_disposable=False,
            )
        )

        with pytest.raises(BadRequestError, match="Invalid email format"):
            await create_user_handler.execute(cmd)

        mock_email_notifications.enqueue.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_user_undeliverable_email(
        self,
        create_user_handler: CreateUserHandler,
        mock_email_verifier,
        mock_email_notifications,
    ):
        cmd = CreateUserCommand(
            username="testuser",
            email="nonexistent@example.com",
            password="TestPassword123!",
        )

        mock_email_verifier.check = AsyncMock(
            return_value=EmailVerificationResult(
                is_valid_format=True,
                is_deliverable=False,
                is_disposable=False,
                details="mailbox_does_not_exist",
            )
        )

        with pytest.raises(BadRequestError, match="Email appears undeliverable"):
            await create_user_handler.execute(cmd)

        mock_email_notifications.enqueue.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_user_disposable_email(
        self,
        create_user_handler: CreateUserHandler,
        mock_email_verifier,
        mock_email_notifications,
    ):
        cmd = CreateUserCommand(
            username="testuser",
            email="user@10minutemail.com",
            password="TestPassword123!",
        )

        mock_email_verifier.check = AsyncMock(
            return_value=EmailVerificationResult(
                is_valid_format=True,
                is_deliverable=True,
                is_disposable=True,
            )
        )

        with pytest.raises(
            BadRequestError, match="Disposable email addresses are not allowed"
        ):
            await create_user_handler.execute(cmd)

        mock_email_notifications.enqueue.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_user_email_verifier_unauthorized(
        self,
        create_user_handler: CreateUserHandler,
        mock_email_verifier,
        mock_email_notifications,
    ):
        cmd = CreateUserCommand(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
        )

        mock_email_verifier.check = AsyncMock(
            return_value=EmailVerificationResult(
                is_valid_format=True,
                is_deliverable=False,
                is_disposable=False,
                details="http_401",
            )
        )

        with pytest.raises(
            ServiceUnavailableError, match="Email verification service unauthorized"
        ):
            await create_user_handler.execute(cmd)

        mock_email_notifications.enqueue.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_user_email_verifier_server_error(
        self,
        create_user_handler: CreateUserHandler,
        mock_email_verifier,
        mock_email_notifications,
    ):
        cmd = CreateUserCommand(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
        )

        mock_email_verifier.check = AsyncMock(
            return_value=EmailVerificationResult(
                is_valid_format=True,
                is_deliverable=False,
                is_disposable=False,
                details="http_500",
            )
        )

        with pytest.raises(
            ServiceUnavailableError, match="Email verification service unavailable"
        ):
            await create_user_handler.execute(cmd)

        mock_email_notifications.enqueue.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_user_email_verifier_timeout(
        self,
        create_user_handler: CreateUserHandler,
        mock_email_verifier,
        mock_email_notifications,
    ):
        cmd = CreateUserCommand(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
        )

        mock_email_verifier.check = AsyncMock(
            return_value=EmailVerificationResult(
                is_valid_format=True,
                is_deliverable=False,
                is_disposable=False,
                details="transient_timeout",
            )
        )

        with pytest.raises(
            ServiceUnavailableError, match="Email verification service unavailable"
        ):
            await create_user_handler.execute(cmd)

        mock_email_notifications.enqueue.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_user_checks_email_before_user_exists(
        self,
        create_user_handler: CreateUserHandler,
        mock_email_verifier,
        mock_users_repository,
        mock_email_notifications,
    ):
        cmd = CreateUserCommand(
            username="testuser",
            email="invalid@example.com",
            password="TestPassword123!",
        )

        mock_email_verifier.check = AsyncMock(
            return_value=EmailVerificationResult(
                is_valid_format=False,
                is_deliverable=False,
                is_disposable=False,
            )
        )

        with pytest.raises(BadRequestError):
            await create_user_handler.execute(cmd)

        mock_users_repository.exists_user.assert_not_called()
        mock_email_notifications.enqueue.assert_not_called()
