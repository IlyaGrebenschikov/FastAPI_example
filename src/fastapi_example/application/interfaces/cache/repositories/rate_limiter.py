from typing import Protocol


class IRateLimiterCacheRepository(Protocol):
    async def get_request_count(self, key: str, window: int, now: float) -> int: ...
