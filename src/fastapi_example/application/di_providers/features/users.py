from dishka import Provider, Scope, provide

from fastapi_example.application.features.users.create_user import CreateUserHandler
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.security import IHasher


class UsersFeaturesProvider(Provider):
    def __init__(self, scope=None, component=None):
        super().__init__(scope, component)

    @provide(scope=Scope.REQUEST)
    def create_user_handler(
        self,
        repository: IUsersRepository,
        hasher: IHasher,
        transaction_manager: ITransactionManager,
    ) -> CreateUserHandler:
        return CreateUserHandler(repository, hasher, transaction_manager)
