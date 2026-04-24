import logging
from dataclasses import asdict

from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
    TCreateUser,
)
from fastapi_example.application.interfaces.security import IHasher
from fastapi_example.application.interfaces.services import IEmailValidatorService
from .command import CreateUserCommand
from fastapi_example.domain.entities import User
from fastapi_example.application.exceptions.http_exceptions import ConflictError

log = logging.getLogger(__name__)


class CreateUserHandler:
    def __init__(
        self,
        repository: IUsersRepository,
        hasher: IHasher,
        transaction_manager: ITransactionManager,
        email_validator: IEmailValidatorService,
    ) -> None:
        self._repository = repository
        self._hasher = hasher
        self._transaction_manager = transaction_manager
        self._email_validator = email_validator

    async def execute(self, cmd: CreateUserCommand) -> User:
        await self._email_validator.validate(cmd.email)

        async with self._transaction_manager:
            if await self._repository.exists_user(
                username=cmd.username, email=cmd.email
            ):
                log.warning(
                    "User creation failed - user already exists with username: '%s' or email: '%s'",
                    cmd.username,
                    cmd.email,
                )
                raise ConflictError(
                    f"User already exists with username: {cmd.username} or email: {cmd.email}"
                )

            cmd.password = self._hasher.hash_password(cmd.password)
            return await self._repository.create_user(TCreateUser(**asdict(cmd)))
