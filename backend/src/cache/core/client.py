import asyncio
from typing import Optional

import redis.asyncio as aioredis

from backend.src.core.settings import RedisSettings, get_redis_settings


def _convert_key(key: Optional[str | int]) -> str:
    return str(key)


class RedisClient:
    def __init__(self, client: aioredis.Redis):
        self._client = client

    async def get_one(self, key: Optional[str | int]) -> Optional[str]:
        return await self._client.get(_convert_key(key))

    async def set_one(self, key: Optional[str | int], value: Optional[str | int]) -> Optional[bool]:
        return await self._client.set(_convert_key(key), _convert_key(value))

    async def set_dict(self, key: Optional[str | int], value: Optional[dict]) -> Optional[int]:
        return await self._client.hset(_convert_key(key), mapping=value)

    async def get_dict_all(self, key: Optional[str | int]) -> Optional[dict]:
        return await self._client.hgetall(_convert_key(key))


def get_redis_client(redis_settings: RedisSettings) -> RedisClient:
    return RedisClient(aioredis.from_url(redis_settings.get_url, decode_responses=True))

