from dishka import Provider, Scope, provide

from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.security import IHasher
from fastapi_example.application.interfaces.services import (
    IAuthService,
    ITokenJWTService,
)
from fastapi_example.application.services import AuthService, TokenJWTService
from fastapi_example.infrastructure.settings import JWTSettings


class AuthServiceProvider(Provider):
    def __init__(self, settings: JWTSettings, scope=None, component=None):
        super().__init__(scope, component)
        self._settings = settings

    @provide(scope=Scope.REQUEST)
    def jwt_token(self) -> ITokenJWTService:
        return TokenJWTService(self._settings)

    @provide(scope=Scope.REQUEST)
    def auth_service(
        self,
        repository: IUsersRepository,
        token_jwt: ITokenJWTService,
        hasher: IHasher,
        transaction_manager: ITransactionManager,
    ) -> IAuthService:
        return AuthService(repository, token_jwt, hasher, transaction_manager)
