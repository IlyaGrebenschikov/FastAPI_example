from dishka import (
    Provider,
    Scope,
    provide
)

from src.application.interfaces.mappers import IUsersServiceMapper
from src.application.interfaces.repositories import IUsersRepository
from src.application.interfaces.services import IUsersService
from src.application.mappers import UserServiceMapper
from src.application.services import UsersService

class ServicesProvider(Provider):
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
    ) -> IUsersService:
        return UsersService(repository, mapper)
