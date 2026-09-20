from uuid import UUID

import redis.asyncio as aioredis

from fastapi_example.application.interfaces.cache.repositories import (
    IRefreshTokenRepository,
)


class RefreshTokenRepository(IRefreshTokenRepository):
    def __init__(self, client: aioredis.Redis, refresh_expiration: int):
        self._redis = client
        self._refresh_expiration = refresh_expiration

    def _key(self, user_id: UUID, jti: str) -> str:
        return f"refresh:{user_id}:{jti}"

    async def save(self, user_id: UUID, jti: str) -> None:
        await self._redis.set(
            self._key(user_id, jti), "1", ex=self._refresh_expiration * 60
        )

    async def revoke(self, user_id: UUID, jti: str) -> bool:
        return bool(await self._redis.delete(self._key(user_id, jti)))
