from dishka import (
    Provider,
    Scope,
    provide
)

from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.mappers import IUsersServiceMapper
from fastapi_example.application.interfaces.database.repositories import IUsersRepository
from fastapi_example.application.interfaces.services import IUsersService, IHasherService, IAuthService
from fastapi_example.application.mappers import UserServiceMapper
from fastapi_example.application.services import UsersService

class UsersServiceProvider(Provider):
    def __init__(self, scope=None, component=None):
        super().__init__(scope, component)

    @provide(scope=Scope.APP)
    def user_service_mapper(self) -> IUsersServiceMapper:
        return UserServiceMapper()

    @provide(scope=Scope.REQUEST)
    def users_service(
            self,
            repository: IUsersRepository,
            mapper: IUsersServiceMapper,
            hasher: IHasherService,
            transaction_manager: ITransactionManager,
            auth: IAuthService,
    ) -> IUsersService:
        return UsersService(repository, mapper, hasher, transaction_manager, auth)
