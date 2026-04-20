from dishka import Provider, Scope, provide

from fastapi_example.application.features.users.create_user import CreateUserHandler
from fastapi_example.application.features.users.get_user import GetUserHandler
from fastapi_example.application.features.users.update_user import UpdateUserHandler
from fastapi_example.application.features.users.delete_user import DeleteUserHandler
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.security import IHasher
from fastapi_example.application.interfaces.services import IEmailValidatorService


class UsersFeaturesProvider(Provider):
    def __init__(self, scope=None, component=None):
        super().__init__(scope, component)

    @provide(scope=Scope.REQUEST)
    def create_user_handler(
        self,
        repository: IUsersRepository,
        hasher: IHasher,
        transaction_manager: ITransactionManager,
        email_validator: IEmailValidatorService,
    ) -> CreateUserHandler:
        return CreateUserHandler(
            repository, hasher, transaction_manager, email_validator
        )

    @provide(scope=Scope.REQUEST)
    def get_user_handler(
        self,
        repository: IUsersRepository,
        transaction_manager: ITransactionManager,
    ) -> GetUserHandler:
        return GetUserHandler(repository, transaction_manager)

    @provide(scope=Scope.REQUEST)
    def update_user_handler(
        self,
        repository: IUsersRepository,
        transaction_manager: ITransactionManager,
        email_validator: IEmailValidatorService,
    ) -> UpdateUserHandler:
        return UpdateUserHandler(repository, transaction_manager, email_validator)

    @provide(scope=Scope.REQUEST)
    def delete_user_handler(
        self,
        repository: IUsersRepository,
        hasher: IHasher,
        transaction_manager: ITransactionManager,
    ) -> DeleteUserHandler:
        return DeleteUserHandler(repository, hasher, transaction_manager)
