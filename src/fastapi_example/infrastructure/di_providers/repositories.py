from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_example.application.interfaces.database.repositories.users import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.mappers.users_repository import (
    IUsersRepositoryMapper,
)
from fastapi_example.infrastructure.database.repositories import (
    SQLAlchemyUsersRepository,
)


class RepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def users_repository(
            self,
            session: AsyncSession,
            mapper: IUsersRepositoryMapper
    ) -> IUsersRepository:
        return SQLAlchemyUsersRepository(session, mapper)
