from collections.abc import AsyncIterator

import redis.asyncio as aioredis
from dishka import Provider, Scope, provide
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from fastapi_example.application.interfaces.cache.repositories import (
    IRateLimiterCacheRepository,
)
from fastapi_example.application.interfaces.communication import IEmailSender
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.http_clients import IEmailVerifier
from fastapi_example.application.interfaces.message_broker.producers import (
    IEmailNotificationsProducer,
)
from fastapi_example.application.interfaces.security import IPwdHasher
from fastapi_example.core.settings import (
    CacheSettings,
    DatabaseSettings,
    EmailVerifierSettings,
    MessageBrokerSettings,
    SMTPSettings,
)
from fastapi_example.infrastructure.cache import create_client
from fastapi_example.infrastructure.cache.repositories import (
    RateLimiterCacheRepository,
)
from fastapi_example.infrastructure.database import (
    TransactionManager,
    create_sa_engine,
    create_sa_session_factory,
)
from fastapi_example.infrastructure.database.repositories import UsersRepository
from fastapi_example.infrastructure.http_clients import (
    AbstractApiEmailVerifier,
    NullEmailVerifier,
)
from fastapi_example.infrastructure.message_broker import create_broker
from fastapi_example.infrastructure.message_broker.producers import (
    EmailNotificationsProducer,
)
from fastapi_example.infrastructure.pwd_hasher import Argon2Hasher
from fastapi_example.infrastructure.smtp import EmailSender, create_smtp_client


class DatabaseProvider(Provider):
    def __init__(self, database_settings: DatabaseSettings, scope=None, component=None):
        super().__init__(scope, component)
        self._database_settings = database_settings

    @provide(scope=Scope.APP)
    def db_engine(self) -> AsyncEngine:
        return create_sa_engine(self._database_settings.url_obj)

    @provide(scope=Scope.APP)
    def db_session_factory(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return create_sa_session_factory(engine)

    @provide(scope=Scope.REQUEST)
    async def db_session(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def transaction_manager(self, session: AsyncSession) -> ITransactionManager:
        return TransactionManager(session)


class RepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def users_repository(self, session: AsyncSession) -> IUsersRepository:
        return UsersRepository(session)


class PwdHasherProvider(Provider):
    @provide(scope=Scope.APP)
    def get_password_hash(self) -> PasswordHash:
        return PasswordHash.recommended()

    @provide(scope=Scope.APP)
    def argon2_hasher(self, hasher: PasswordHash) -> IPwdHasher:
        return Argon2Hasher(hasher)


class CacheProvider(Provider):
    def __init__(self, cache_settings: CacheSettings, scope=None, component=None):
        super().__init__(scope, component)
        self._cache_settings = cache_settings

    @provide(scope=Scope.APP)
    def client(self) -> aioredis.Redis:
        return create_client(self._cache_settings.url)


class CacheRepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def rate_limiter_cache_repository(
        self, redis_client: aioredis.Redis
    ) -> IRateLimiterCacheRepository:
        return RateLimiterCacheRepository(redis_client)


class CommunicationProvider(Provider):
    def __init__(self, smtp_settings: SMTPSettings, scope=None, component=None):
        super().__init__(scope, component)
        self._smtp_settings = smtp_settings

    @provide(scope=Scope.APP)
    async def smtp_client(self):
        client = create_smtp_client(self._smtp_settings)
        async with client:
            if self._smtp_settings.username and self._smtp_settings.password:
                await client.login(
                    self._smtp_settings.username, self._smtp_settings.password
                )
            yield client

    @provide(scope=Scope.APP)
    def email_sender(self, client) -> IEmailSender:
        return EmailSender(client)


class HTTPClientsProvider(Provider):
    def __init__(
        self, email_verifier_settings: EmailVerifierSettings, scope=None, component=None
    ):
        self._email_verifier_settings = email_verifier_settings
        super().__init__(scope, component)

    @provide(scope=Scope.APP)
    def email_verifier(self) -> IEmailVerifier:
        if not self._email_verifier_settings.enabled:
            return NullEmailVerifier()
        return AbstractApiEmailVerifier(self._email_verifier_settings.api_key)


class MessageBrokerProvider(Provider):
    def __init__(
        self, broker_settings: MessageBrokerSettings, scope=None, component=None
    ):
        super().__init__(scope, component)
        self._broker_settings = broker_settings

    @provide(scope=Scope.APP)
    def client(self):
        return create_broker(self._broker_settings)


class MessageBrokerProducersProvider(Provider):
    @provide(scope=Scope.APP)
    def email_notifications_producer(
        self, broker
    ) -> IEmailNotificationsProducer:
        return EmailNotificationsProducer(broker)
