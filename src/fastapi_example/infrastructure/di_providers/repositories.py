import redis.asyncio as aioredis
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_example.application.interfaces.cache.repositories import (
    IRateLimiterCacheRepository,
)
from fastapi_example.application.interfaces.database.repositories.users import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.database.mappers import (
    IUsersRepositoryMapper,
)
from fastapi_example.infrastructure.cache.repositories import RateLimiterCacheRepository
from fastapi_example.infrastructure.database.repositories import (
    SQLAlchemyUsersRepository,
)


class RepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def users_repository(
        self, session: AsyncSession, mapper: IUsersRepositoryMapper
    ) -> IUsersRepository:
        return SQLAlchemyUsersRepository(session, mapper)

    @provide(scope=Scope.REQUEST)
    def rate_limiter_cache_repository(
        self, redis_client: aioredis.Redis
    ) -> IRateLimiterCacheRepository:
        return RateLimiterCacheRepository(redis_client)
