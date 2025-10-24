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

from src.application.interfaces.factories import IRepositoriesFactory
from src.application.interfaces.repositories.users import IUsersRepository
from src.application.interfaces.mappers.users_repository import IUsersRepositoryMapper
from src.infrastructure import InfrastructureSettings
from src.infrastructure.database import (
    create_sa_engine,
    create_sa_session_factory
)
from src.infrastructure.database.repositories import RepositoryFactory
from src.infrastructure.database.mappers import UsersRepositoryMapper


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

    @provide(scope=Scope.APP)
    def users_repository_mapper(self) -> IUsersRepositoryMapper:
        return UsersRepositoryMapper()

    @provide(scope=Scope.APP)
    def repository_factory(self) -> IRepositoriesFactory:
        return RepositoryFactory()

    @provide(scope=Scope.REQUEST)
    def users_repository(
            self,
            repository_factory: IRepositoriesFactory,
            session_factory: async_sessionmaker[AsyncSession],
            mapper: IUsersRepositoryMapper
    ) -> IUsersRepository:
        return repository_factory.create_user_repository(session_factory, mapper)
