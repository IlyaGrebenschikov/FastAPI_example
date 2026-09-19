from dishka import Provider, Scope, provide

from fastapi_example.application.interfaces.cache.repositories import (
    IRefreshTokenRepository,
)
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces import IPwdHasher
from fastapi_example.application.interfaces.services import (
    ITokenJWTService,
)
from fastapi_example.application.features.auth.commands import (
    LoginEmailHandler,
    LogoutHandler,
    RefreshHandler,
)


class AuthFeaturesProvider(Provider):
    def __init__(self, scope=None, component=None):
        super().__init__(scope, component)

    @provide(scope=Scope.REQUEST)
    def login_email_handler(
        self,
        users_repository: IUsersRepository,
        hasher: IPwdHasher,
        token_service: ITokenJWTService,
        refresh_token_repository: IRefreshTokenRepository,
        transaction_manager: ITransactionManager,
    ) -> LoginEmailHandler:
        return LoginEmailHandler(
            users_repository, hasher, token_service, refresh_token_repository, transaction_manager
        )

    @provide(scope=Scope.REQUEST)
    def logout_handler(
        self,
        refresh_token_repository: IRefreshTokenRepository,
    ) -> LogoutHandler:
        return LogoutHandler(refresh_token_repository)

    @provide(scope=Scope.REQUEST)
    def refresh_handler(
        self,
        users_repository: IUsersRepository,
        refresh_token_repository: IRefreshTokenRepository,
        token_service: ITokenJWTService,
        transaction_manager: ITransactionManager,
    ) -> RefreshHandler:
        return RefreshHandler(
            users_repository, refresh_token_repository, token_service, transaction_manager
        )
