import time

from fastapi_example.application.exceptions.http_exceptions import TooManyRequestsError
from fastapi_example.application.interfaces.cache.repositories import (
    IRateLimiterCacheRepository,
)
from fastapi_example.application.interfaces.services import IRateLimiterService


class RateLimiterService(IRateLimiterService):
    def __init__(self, cache_repository: IRateLimiterCacheRepository) -> None:
        self._cache_repository = cache_repository

    async def check(self, identifier: str, path: str, limit: int, window: int):
        key = f"rl:{identifier}:{path}"
        now = time.time()
        count = await self._cache_repository.get_request_count(key, window, now)
        if count > limit:
            raise TooManyRequestsError("Too many requests")
