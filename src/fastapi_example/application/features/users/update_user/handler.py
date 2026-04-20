import logging
from dataclasses import asdict
from typing import cast

from fastapi_example.domain.entities import User
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
    TUpdateUser,
)
from fastapi_example.application.exceptions.http_exceptions import (
    NotFoundError,
    ConflictError,
)
from .command import UpdateUserCommand

log = logging.getLogger(__name__)


class UpdateUserHandler:
    def __init__(
        self, repository: IUsersRepository, transaction_manager: ITransactionManager
    ):
        self._repository = repository
        self._transaction_manager = transaction_manager

    async def execute(self, cmd: UpdateUserCommand) -> User:
        async with self._transaction_manager:
            user = await self._repository.get_user(user_id=cmd.user_id, for_update=True)
            if not user:
                log.warning("User does not exist with ID: '%s'", cmd.user_id)
                raise NotFoundError("User not found")

            if cmd.username:
                if (
                    cmd.username != user.username
                ) and await self._repository.exists_user(username=cmd.username):
                    log.warning(
                        "User update failed - user already exists with username: '%s'",
                        cmd.username,
                    )
                    raise ConflictError(
                        f"User already exists with username: {cmd.username}"
                    )

            if cmd.email:
                if (cmd.email != user.email) and await self._repository.exists_user(
                    email=cmd.email
                ):
                    log.warning(
                        "User update failed - user already exists with email: '%s'",
                        cmd.email,
                    )
                    raise ConflictError(f"User already exists with email: {cmd.email}")

            raw_data = {
                k: v for k, v in asdict(cmd).items() if v is not None and k != "user_id"
            }
            data = cast(TUpdateUser, cast(object, raw_data))
            return await self._repository.update_user(cmd.user_id, data)
