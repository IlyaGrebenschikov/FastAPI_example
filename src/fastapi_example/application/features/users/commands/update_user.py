import logging
from dataclasses import dataclass
from uuid import UUID

from fastapi_example.application.http_exceptions import (
    ConflictError,
    NotFoundError,
)
from fastapi_example.application.interfaces import IPwdHasher
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
    TUpdateUser,
)
from fastapi_example.application.interfaces.services import (
    IEmailNotificationsService,
    IEmailValidatorService,
    TEmailMessage,
)
from fastapi_example.domain import User

log = logging.getLogger(__name__)


@dataclass
class UpdateUserCommand:
    user_id: UUID
    email: str | None = None
    password: str | None = None


class UpdateUserHandler:
    def __init__(
        self,
        users_repository: IUsersRepository,
        hasher: IPwdHasher,
        transaction_manager: ITransactionManager,
        email_validator: IEmailValidatorService,
        email_notifications: IEmailNotificationsService,
    ) -> None:
        self._users_repository = users_repository
        self._hasher = hasher
        self._transaction_manager = transaction_manager
        self._email_validator = email_validator
        self._email_notifications = email_notifications

    async def execute(self, cmd: UpdateUserCommand) -> User:
        async with self._transaction_manager:
            user = await self._users_repository.get_user(
                user_id=cmd.user_id, for_update=True
            )
            if not user:
                log.warning("User does not exist with ID: '%s'", cmd.user_id)
                raise NotFoundError("User not found")

            if cmd.email is not None and cmd.email != user.email:
                if await self._users_repository.exists_user(email=cmd.email):
                    log.warning(
                        "User update failed - user already exists with email: '%s'",
                        cmd.email,
                    )
                    raise ConflictError(f"User already exists with email: {cmd.email}")

                await self._email_validator.validate(cmd.email)

            update_data: TUpdateUser = {}
            if cmd.email is not None and cmd.email != user.email:
                update_data["email"] = cmd.email
            if cmd.password is not None:
                update_data["password"] = self._hasher.hash_password(cmd.password)

            updated = await self._users_repository.update_user(cmd.user_id, update_data)

        if updated is None:
            raise NotFoundError("User not found")

        await self._email_notifications.enqueue(
            TEmailMessage(
                recipient=updated.email,
                subject="Account updated",
                content="Hello!\n\nYour account details have been updated.",
            )
        )
        return updated
