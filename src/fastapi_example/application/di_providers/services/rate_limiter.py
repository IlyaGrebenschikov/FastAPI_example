from dishka import Provider, Scope, provide

from fastapi_example.application.interfaces.cache.repositories import (
    IRateLimiterCacheRepository,
)
from fastapi_example.application.interfaces.services import IRateLimiterService
from fastapi_example.application.services import RateLimiterService


class RateLimiterServiceProvider(Provider):
    def __init__(self, scope=None, component=None):
        super().__init__(scope, component)

    @provide(scope=Scope.REQUEST)
    def rate_limiter_service(self, repository: IRateLimiterCacheRepository) -> IRateLimiterService:
        return RateLimiterService(repository)
