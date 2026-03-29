import logging

from fastapi_example.application.dto import Token
from fastapi_example.application.exceptions.http_exceptions import UnAuthorizedError
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.dto import TokenPayload, LoginCredentials
from fastapi_example.application.interfaces.security import IHasher
from fastapi_example.application.interfaces.services import (
    IAuthService,
    ITokenJWTService,
)

log = logging.getLogger(__name__)


class AuthService(IAuthService):
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

    async def login(self, credentials: LoginCredentials) -> Token:
        async with self._transaction_manager:
            if not await self._user_repository.exists_user(
                username=credentials.username
            ):
                log.warning("User not found with username '%s'", credentials.username)
                raise UnAuthorizedError("Incorrect login or password")

            user = await self._user_repository.get_user(username=credentials.username)

        if not self._hasher.verify_password(credentials.password, user.password):
            log.debug("Password verification failed")
            raise UnAuthorizedError("Incorrect login or password")

        token_payload: TokenPayload = {"sub": str(user.id)}
        if credentials.scopes is not None:
            token_payload["scopes"] = credentials.scopes
        access_token = self._token_jwt.create_access_token(token_payload)

        log.info(
            "User '%s' (ID: %s) successfully logged in", credentials.username, user.id
        )
        return Token(access_token=access_token, token_type="Bearer")
