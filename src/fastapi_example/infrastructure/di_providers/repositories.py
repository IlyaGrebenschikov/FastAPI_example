from dishka import Provider, Scope, provide

from fastapi_example.application.interfaces.database import ITransactionManager
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
            transaction_manager: ITransactionManager,
            mapper: IUsersRepositoryMapper
    ) -> IUsersRepository:
        return SQLAlchemyUsersRepository(transaction_manager.session, mapper)
