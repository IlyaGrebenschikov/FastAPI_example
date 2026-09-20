import logging
from dataclasses import dataclass

from fastapi_example.application.http_exceptions import ConflictError
from fastapi_example.application.interfaces import IPwdHasher
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
    TCreateUser,
)
from fastapi_example.application.interfaces.services import (
    IEmailNotificationsService,
    IEmailValidatorService,
    TEmailMessage,
)
from fastapi_example.domain import User

log = logging.getLogger(__name__)


@dataclass
class CreateUserCommand:
    email: str
    password: str


class CreateUserHandler:
    def __init__(
        self,
        repository: IUsersRepository,
        hasher: IPwdHasher,
        transaction_manager: ITransactionManager,
        email_validator: IEmailValidatorService,
        email_notifications: IEmailNotificationsService,
    ) -> None:
        self._repository = repository
        self._hasher = hasher
        self._transaction_manager = transaction_manager
        self._email_validator = email_validator
        self._email_notifications = email_notifications

    async def execute(self, cmd: CreateUserCommand) -> User:
        await self._email_validator.validate(cmd.email)

        async with self._transaction_manager:
            if await self._repository.exists_user(email=cmd.email):
                log.warning(
                    "User creation failed - user already exists with email: '%s'",
                    cmd.email,
                )
                raise ConflictError(f"User already exists with email: {cmd.email}")

            hashed_password = self._hasher.hash_password(cmd.password)
            user = await self._repository.create_user(
                TCreateUser(email=cmd.email, password=hashed_password)
            )

        await self._email_notifications.enqueue(
            TEmailMessage(
                recipient=user.email,
                subject="Account created",
                content="Hello!\n\nYour account has been created successfully.",
            )
        )
        return user
