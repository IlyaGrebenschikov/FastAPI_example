import logging
from dataclasses import asdict
from typing import cast

from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
    TCreateUser,
)
from fastapi_example.application.interfaces.security import IHasher
from fastapi_example.application.interfaces.http_clients import IEmailVerifier
from .command import CreateUserCommand
from fastapi_example.domain.entities import User
from fastapi_example.application.exceptions.http_exceptions import ConflictError, BadRequestError, ServiceUnavailableError

log = logging.getLogger(__name__)


class CreateUserHandler:
    def __init__(
        self,
        repository: IUsersRepository,
        hasher: IHasher,
        transaction_manager: ITransactionManager,
        email_verifier: IEmailVerifier,
    ) -> None:
        self._repository = repository
        self._hasher = hasher
        self._transaction_manager = transaction_manager
        self._email_verifier = email_verifier

    async def execute(self, cmd: CreateUserCommand) -> User:
        ver = await self._email_verifier.check(cmd.email)
        if ver.details and ver.details.startswith("http_401"):
            log.error("Email verifier unauthorized (401) for email=%s", cmd.email)
            raise ServiceUnavailableError("Email verification service unauthorized")
        if ver.details and ver.details.startswith(("transient", "network", "http_5")):
            raise ServiceUnavailableError("Email verification service unavailable")
        if not ver.is_valid_format:
            raise BadRequestError(f"Invalid email format: {cmd.email}")
        if not ver.is_deliverable:
            raise BadRequestError("Email appears undeliverable")
        if ver.is_disposable:
            raise BadRequestError("Disposable email addresses are not allowed")

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
            data = cast(TCreateUser, cast(object, asdict(cmd)))
            return await self._repository.create_user(data)
