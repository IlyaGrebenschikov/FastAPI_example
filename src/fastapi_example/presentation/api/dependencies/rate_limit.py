from typing import Annotated

from dishka.integrations.fastapi import FromDishka
from fastapi import Request

from fastapi_example.application.interfaces.services import IRateLimiterService

DEFAULT_RATE_LIMIT = 100
DEFAULT_WINDOW = 60


async def rate_limit(
    request: Request,
    rate_limiter: FromDishka[IRateLimiterService],
) -> None:
    client_ip = request.client.host if request.client else "unknown"
    await rate_limiter.check(
        identifier=client_ip,
        path=request.url.path,
        limit=DEFAULT_RATE_LIMIT,
        window=DEFAULT_WINDOW,
    )


RateLimitDep = Annotated[None, rate_limit]
