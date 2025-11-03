import logging

from fastapi.security import OAuth2PasswordRequestForm

from src.application.dto import Token
from src.application.exceptions.http_exceptions import UnAuthorizedError
from src.application.interfaces.services import (
    IAuthService,
    ITokenJWTService,
    IHasherService
)
from src.application.interfaces.database import ITransactionManager
from src.application.interfaces.database.repositories import IUsersRepository

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

        access_token = self._token_jwt.create_access_token({"sub": str(user.id), "scopes": query.scopes})
        log.debug("Access token created")

        return Token(access_token=access_token, token_type="Bearer")

    def get_sub_from_token(self, token: str) -> str:
        return str(self._token_jwt.verify_token(token)["sub"])
