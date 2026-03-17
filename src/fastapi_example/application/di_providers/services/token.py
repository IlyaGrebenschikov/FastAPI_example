from dishka import Provider, Scope, provide

from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.services import (
    ITokenJWTService,
    ITokenService,
)
from fastapi_example.application.services import TokenService


class TokenServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def token_service(
            self,
            repository: IUsersRepository,
            token_jwt: ITokenJWTService,
            transaction_manager: ITransactionManager,
    ) -> ITokenService:
        return TokenService(repository, token_jwt, transaction_manager)
