import logging
from dataclasses import dataclass
from uuid import UUID

from fastapi_example.application.http_exceptions import (
    ForbiddenError,
    NotFoundError,
)
from fastapi_example.application.interfaces import IPwdHasher
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.services import (
    IEmailNotificationsService,
    TEmailMessage,
)
from fastapi_example.domain import User

log = logging.getLogger(__name__)


@dataclass
class DeleteUserCommand:
    user_id: UUID
    password: str


class DeleteUserHandler:
    def __init__(
        self,
        users_repository: IUsersRepository,
        hasher: IPwdHasher,
        transaction_manager: ITransactionManager,
        email_notifications: IEmailNotificationsService,
    ) -> None:
        self._users_repository = users_repository
        self._hasher = hasher
        self._transaction_manager = transaction_manager
        self._email_notifications = email_notifications

    async def execute(self, cmd: DeleteUserCommand) -> User:
        async with self._transaction_manager:
            user = await self._users_repository.get_user(
                user_id=cmd.user_id, for_update=True
            )
            if not user:
                log.warning("User does not exist with ID: '%s'", cmd.user_id)
                raise NotFoundError("User not found")

            if not self._hasher.verify_password(cmd.password, user.password):
                log.warning(
                    "User deletion failed - incorrect password for user ID: '%s'",
                    cmd.user_id,
                )
                raise ForbiddenError("Incorrect password")

            result = await self._users_repository.delete_user(user_id=cmd.user_id)

        if result is None:
            raise NotFoundError("User not found")

        await self._email_notifications.enqueue(
            TEmailMessage(
                recipient=result.email,
                subject="Account deleted",
                content="Hello!\n\nYour account has been deleted.",
            )
        )
        log.info("User deleted with ID: %s", result.id)
        return result
