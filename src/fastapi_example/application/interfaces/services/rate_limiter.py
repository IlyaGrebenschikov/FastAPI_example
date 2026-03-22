from typing import Protocol


class IRateLimiterService(Protocol):
    async def check(self, identifier: str, path: str, limit: int, window: int): ...
