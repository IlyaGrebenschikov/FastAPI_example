import logging
from dataclasses import dataclass

from fastapi_example.application.http_exceptions import UnAuthorizedError
from fastapi_example.application.interfaces import IPwdHasher
from fastapi_example.application.interfaces.cache.repositories import (
    IRefreshTokenRepository,
)
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.services import (
    ITokenJWTService,
    TokenPair,
)

log = logging.getLogger(__name__)


@dataclass
class LoginEmailCommand:
    email: str
    password: str


class LoginEmailHandler:
    def __init__(
        self,
        users_repository: IUsersRepository,
        hasher: IPwdHasher,
        token_service: ITokenJWTService,
        refresh_token_repository: IRefreshTokenRepository,
        transaction_manager: ITransactionManager,
    ) -> None:
        self._users_repository = users_repository
        self._hasher = hasher
        self._token_service = token_service
        self._refresh_token_repository = refresh_token_repository
        self._transaction_manager = transaction_manager

    async def execute(self, cmd: LoginEmailCommand) -> TokenPair:
        async with self._transaction_manager:
            user = await self._users_repository.get_user(email=cmd.email)
            if not user:
                log.warning("User not found with email '%s'", cmd.email)
                raise UnAuthorizedError("Incorrect login or password")

            if not self._hasher.verify_password(cmd.password, user.password):
                log.debug("Password verification failed")
                raise UnAuthorizedError("Incorrect login or password")

            user_id = user.id

        pair = self._token_service.create_token_pair(user_id)
        await self._refresh_token_repository.save(user_id, pair.jti)
        return pair
