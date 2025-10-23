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

from src.infrastructure import InfrastructureSettings
from src.infrastructure.database import (
    create_sa_engine,
    create_sa_session_factory
)

class InfrastructureProvider(Provider):
    def __init__(
            self,
            infrastructure_settings: InfrastructureSettings,
            scope = None,
            component = None
    ):
        super().__init__(scope, component)
        self._infrastructure_settings = infrastructure_settings

    @provide(scope=Scope.APP)
    def db_engine(self) -> AsyncEngine:
        return create_sa_engine(self._infrastructure_settings.database.url_obj)

    @provide(scope=Scope.APP)
    def db_session(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_sa_session_factory(engine)
