from dishka import Provider, Scope, provide

from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.security import IHasher
from fastapi_example.application.interfaces.services import (
    ITokenJWTService,
)
from fastapi_example.application.features.auth.create_access_token import CreateAccessTokenHandler


class AuthFeaturesProvider(Provider):
    def __init__(self, scope=None, component=None):
        super().__init__(scope, component)

    @provide(scope=Scope.REQUEST)
    def create_access_token_handler(
        self,
        repository: IUsersRepository,
        token_jwt: ITokenJWTService,
        hasher: IHasher,
        transaction_manager: ITransactionManager,
    ) -> CreateAccessTokenHandler:
        return CreateAccessTokenHandler(repository, token_jwt, hasher, transaction_manager)
