from typing import Protocol
from uuid import UUID


class IRefreshTokenRepository(Protocol):
    async def save(self, user_id: UUID, jti: str) -> None: ...

    async def revoke(self, user_id: UUID, jti: str) -> bool: ...
