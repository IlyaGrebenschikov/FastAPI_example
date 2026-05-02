import logging

from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.security import IHasher
from fastapi_example.application.interfaces.services import (
    IEmailNotificationsService,
    TEmailMessage,
)
from .command import DeleteUserCommand
from fastapi_example.domain.entities import User
from fastapi_example.application.exceptions.http_exceptions import (
    NotFoundError,
    ForbiddenError,
)

log = logging.getLogger(__name__)


class DeleteUserHandler:
    def __init__(
        self,
        repository: IUsersRepository,
        hasher: IHasher,
        transaction_manager: ITransactionManager,
        email_notifications: IEmailNotificationsService,
    ):
        self._repository = repository
        self._hasher = hasher
        self._transaction_manager = transaction_manager
        self._email_notifications = email_notifications

    async def execute(self, cmd: DeleteUserCommand) -> User:
        async with self._transaction_manager:
            user = await self._repository.get_user(user_id=cmd.user_id, for_update=True)
            if not user:
                log.warning("User does not exist with ID: '%s'", cmd.user_id)
                raise NotFoundError("User not found")

            if not self._hasher.verify_password(cmd.password, user.password):
                log.warning(
                    "User deletion failed - incorrect password confirmation for user ID: '%s'",
                    cmd.user_id,
                )
                raise ForbiddenError("Incorrect password confirmation")

            result = await self._repository.delete_user(user_id=cmd.user_id)

        await self._email_notifications.enqueue(
            TEmailMessage(
                recipient=result.email,
                subject="Account deleted",
                content=(
                    f"Hello, {result.username}!\n\n"
                    "Your account has been deleted."
                ),
            )
        )
        log.info("User deleted with ID: %s", result.id)
        return result
