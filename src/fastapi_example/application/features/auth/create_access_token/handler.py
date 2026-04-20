import logging

from fastapi_example.application.exceptions.http_exceptions import UnAuthorizedError
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.security import IHasher
from fastapi_example.application.interfaces.services import (
    ITokenJWTService,
    TTokenPayload,
)
from .command import CreateAccessTokenCommand

log = logging.getLogger(__name__)


class CreateAccessTokenHandler:
    def __init__(
        self,
        user_repository: IUsersRepository,
        token_jwt: ITokenJWTService,
        hasher: IHasher,
        transaction_manager: ITransactionManager,
    ) -> None:
        self._user_repository = user_repository
        self._token_jwt = token_jwt
        self._hasher = hasher
        self._transaction_manager = transaction_manager

    async def execute(self, cmd: CreateAccessTokenCommand) -> str:
        async with self._transaction_manager:
            user = await self._user_repository.get_user(username=cmd.username)
            if not user:
                log.warning("User not found with username '%s'", cmd.username)
                raise UnAuthorizedError("Incorrect login or password")

        if not self._hasher.verify_password(cmd.password, user.password):
            log.debug("Password verification failed")
            raise UnAuthorizedError("Incorrect login or password")

        token_payload: TTokenPayload = {"sub": str(user.id)}
        if cmd.scopes is not None:
            token_payload["scopes"] = cmd.scopes
        access_token = self._token_jwt.create_access_token(token_payload)

        log.info(
            "User '%s' (ID: %s) successfully logged in", cmd.username, user.id
        )
        return access_token
