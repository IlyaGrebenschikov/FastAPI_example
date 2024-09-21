from typing import Optional, Type
from datetime import timedelta

import redis.asyncio as aioredis

from backend.src.core.settings import RedisSettings


class RedisClient:
    def __init__(self, client: aioredis.Redis) -> None:
        self._client = client

    @classmethod
    def from_url(cls: Type['RedisClient'], url: str) -> 'RedisClient':
        return cls(
            client=aioredis.from_url(
                url,
                decode_responses=True
            )
        )

    @staticmethod
    def _convert_key(key: Optional[str | int]) -> str:
        return str(key)

    async def get_one(self, key: Optional[str | int]) -> Optional[str]:
        return await self._client.get(self._convert_key(key))

    async def set_one(
            self,
            key: Optional[str | int],
            value: Optional[str | int],
            expire: Optional[timedelta | int]
    ) -> Optional[bool]:
        return await self._client.set(self._convert_key(key), self._convert_key(value), ex=expire)

    async def set_dict(self, key: Optional[str | int], value: Optional[dict]) -> Optional[int]:
        return await self._client.hset(self._convert_key(key), mapping=value)

    async def get_dict_all(self, key: Optional[str | int]) -> Optional[dict]:
        return await self._client.hgetall(self._convert_key(key))

    async def delete(self, *keys: Optional[str | int]) -> Optional[int]:
        return await self._client.delete(*{self._convert_key(key) for key in keys})

    async def set_expire(self, key: Optional[str | int], time: Optional[timedelta | int]) -> Optional[bool]:
        return await self._client.expire(self._convert_key(key), time)

    async def get_ttl(self, key: Optional[str | int]) -> Optional[int]:
        return await self._client.ttl(self._convert_key(key))
