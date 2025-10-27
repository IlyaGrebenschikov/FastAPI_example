import logging
from typing import AsyncGenerator, Any

from dishka import (
    Provider,
    Scope,
    provide
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker
)

from src.application.interfaces.database import ITransactionManager
from src.application.interfaces.database.repositories.users import IUsersRepository
from src.application.interfaces.mappers.users_repository import IUsersRepositoryMapper
from src.infrastructure import InfrastructureSettings
from src.infrastructure.database import (
    create_sa_engine,
    create_sa_session_factory,
    TransactionManager,
)
from src.infrastructure.database.mappers import UsersRepositoryMapper
from src.infrastructure.database.repositories import SQLAlchemyUserRepository

log = logging.getLogger(__name__)


class DatabaseProvider(Provider):
    def __init__(
            self,
            infrastructure_settings: InfrastructureSettings,
            scope=None,
            component=None
    ):
        super().__init__(scope, component)
        self._infrastructure_settings = infrastructure_settings

    @provide(scope=Scope.APP)
    def db_engine(self) -> AsyncEngine:
        return create_sa_engine(self._infrastructure_settings.database.url_obj)

    @provide(scope=Scope.APP)
    def db_session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_sa_session_factory(engine)

    @provide(scope=Scope.REQUEST)
    def transaction_manager(self, session_factory: async_sessionmaker[AsyncSession]) -> ITransactionManager:
        return TransactionManager(session_factory)

    @provide(scope=Scope.APP)
    def users_repository_mapper(self) -> IUsersRepositoryMapper:
        return UsersRepositoryMapper()

    @provide(scope=Scope.REQUEST)
    def users_repository(
            self,
            transaction_manager: ITransactionManager,
            mapper: IUsersRepositoryMapper
    ) -> IUsersRepository:
        return SQLAlchemyUserRepository(transaction_manager.session, mapper)
