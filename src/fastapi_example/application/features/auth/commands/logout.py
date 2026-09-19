from dataclasses import dataclass
from uuid import UUID

from fastapi_example.application.http_exceptions import UnAuthorizedError
from fastapi_example.application.interfaces.cache.repositories import (
    IRefreshTokenRepository,
)


@dataclass
class LogoutCommand:
    user_id: UUID
    jti: str


class LogoutHandler:
    def __init__(self, refresh_token_repository: IRefreshTokenRepository):
        self._refresh_token_repository = refresh_token_repository

    async def execute(self, cmd: LogoutCommand) -> None:
        if not await self._refresh_token_repository.revoke(cmd.user_id, cmd.jti):
            raise UnAuthorizedError("Refresh token not found")
