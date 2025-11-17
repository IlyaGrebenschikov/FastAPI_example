import logging

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker
)

from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories.users import IUsersRepository
from fastapi_example.application.interfaces.mappers.users_repository import IUsersRepositoryMapper
from fastapi_example.infrastructure import InfrastructureSettings
from fastapi_example.infrastructure.database import (
    TransactionManager,
    create_sa_engine,
    create_sa_session_factory,
)
from fastapi_example.infrastructure.database.mappers import UsersRepositoryMapper
from fastapi_example.infrastructure.database.repositories import SQLAlchemyUserRepository

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
