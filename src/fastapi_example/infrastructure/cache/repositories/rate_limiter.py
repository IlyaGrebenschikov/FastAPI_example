import uuid

import redis.asyncio as aioredis

from fastapi_example.application.interfaces.cache.repositories import (
    IRateLimiterCacheRepository,
)


class RateLimiterCacheRepository(IRateLimiterCacheRepository):
    def __init__(self, client: aioredis.Redis) -> None:
        self._client = client

    async def get_request_count(self, key: str, window: int, now: float) -> int:
        async with self._client.pipeline() as pipe:
            await pipe.zremrangebyscore(key, 0, now - window)
            await pipe.zadd(key, {f"{now}:{uuid.uuid4()}": now})
            await pipe.zcard(key)
            await pipe.expire(key, window)
            results = await pipe.execute()
        return results[2]
