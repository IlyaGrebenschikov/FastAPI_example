import logging
from dataclasses import dataclass
from uuid import UUID

from fastapi_example.application.http_exceptions import NotFoundError, UnAuthorizedError
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
class RefreshCommand:
    user_id: UUID
    jti: str


class RefreshHandler:
    def __init__(
        self,
        user_repository: IUsersRepository,
        refresh_token_repository: IRefreshTokenRepository,
        token_service: ITokenJWTService,
        transaction_manager: ITransactionManager,
    ) -> None:
        self._user_repository = user_repository
        self._refresh_token_repository = refresh_token_repository
        self._token_service = token_service
        self._transaction_manager = transaction_manager

    async def execute(self, cmd: RefreshCommand) -> TokenPair:
        async with self._transaction_manager:
            user = await self._user_repository.get_user(user_id=cmd.user_id)
            if not user:
                log.warning("User not found with id '%s'", cmd.user_id)
                raise NotFoundError("User not found")

        if not await self._refresh_token_repository.revoke(cmd.user_id, cmd.jti):
            raise UnAuthorizedError("Refresh token is invalid or already revoked")

        pair = self._token_service.create_token_pair(user.id)
        await self._refresh_token_repository.save(user.id, pair.jti)
        return pair
