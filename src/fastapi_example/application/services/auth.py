import logging

from fastapi.security import OAuth2PasswordRequestForm

from fastapi_example.application.dto import Token
from fastapi_example.application.exceptions.http_exceptions import UnAuthorizedError
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import IUsersRepository
from fastapi_example.application.interfaces.services import (
    IAuthService,
    ITokenJWTService,
    IHasherService
)
from fastapi_example.application.types import TokenPayload

log = logging.getLogger(__name__)


class AuthService(IAuthService):
    def __init__(
            self,
            user_repository: IUsersRepository,
            token_jwt: ITokenJWTService,
            hasher: IHasherService,
            transaction_manager: ITransactionManager
    ) -> None:
        self._user_repository = user_repository
        self._token_jwt = token_jwt
        self._hasher = hasher
        self._transaction_manager = transaction_manager

    async def login(self, query: OAuth2PasswordRequestForm) -> Token:
        async with self._transaction_manager:
            user = await self._user_repository.get_user(username=query.username)

        if not self._hasher.verify_password(query.password, user.password):
            log.debug("Password verification failed")
            raise UnAuthorizedError("Incorrect login or password")

        token_payload: TokenPayload = {
            "sub": str(user.id),
            "scopes": query.scopes
        }
        access_token = self._token_jwt.create_access_token(token_payload)

        log.info(
            "User '%s' (ID: %s) successfully logged in",
            query.username,
            user.id
        )
        return Token(access_token=access_token, token_type="Bearer")

    async def get_sub_from_token(self, token: str) -> str:
        token_data = self._token_jwt.verify_token(token)
        sub = token_data.get("sub")

        if not sub:
            log.warning("Token missing subject field")
            raise UnAuthorizedError('Token missing subject')

        async with self._transaction_manager.read_only():
            if not await self._user_repository.exists_user(user_id=sub):
                log.warning(
                    "Token validation failed - user does not exist with ID: '%s'",
                    sub
                )
                raise UnAuthorizedError("User not found")

        log.debug("Extracted and verified subject '%s' from token", sub)
        return sub
