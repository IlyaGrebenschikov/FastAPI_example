from dishka import Provider, Scope, provide

from fastapi_example.application.interfaces.database.repositories.mappers import (
    IUsersRepositoryMapper,
)
from fastapi_example.infrastructure.database.repositories.mappers import (
    UsersRepositoryMapper,
)


class MappersProvider(Provider):
    @provide(scope=Scope.APP)
    def users_repository_mapper(self) -> IUsersRepositoryMapper:
        return UsersRepositoryMapper()
