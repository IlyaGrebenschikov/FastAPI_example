from dishka import Provider, Scope, provide

from fastapi_example.application.features.auth.commands import (
    LoginEmailHandler,
    LogoutHandler,
    RefreshHandler,
)
from fastapi_example.application.features.auth.services.token_jwt import TokenJWTService
from fastapi_example.application.features.users.commands import (
    CreateUserHandler,
    DeleteUserHandler,
    UpdateUserHandler,
)
from fastapi_example.application.features.users.queries import (
    GetUserHandler,
)
from fastapi_example.application.features.users.services import EmailValidatorService
from fastapi_example.application.interfaces import IEmailSender, IPwdHasher
from fastapi_example.application.interfaces.cache.repositories import (
    IRateLimiterCacheRepository,
    IRefreshTokenRepository,
)
from fastapi_example.application.interfaces.database import ITransactionManager
from fastapi_example.application.interfaces.database.repositories import (
    IUsersRepository,
)
from fastapi_example.application.interfaces.http_clients import IEmailVerifier
from fastapi_example.application.interfaces.message_broker.producers import (
    IEmailNotificationsProducer,
)
from fastapi_example.application.interfaces.services import (
    IEmailNotificationsService,
    IEmailValidatorService,
    IRateLimiterService,
    ITokenJWTService,
)
from fastapi_example.application.services import (
    EmailNotificationsService,
    RateLimiterService,
)
from fastapi_example.core.settings import JWTSettings, SMTPSettings


class UsersFeaturesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def email_validator_service(
        self, email_verifier: IEmailVerifier
    ) -> IEmailValidatorService:
        return EmailValidatorService(email_verifier)

    @provide(scope=Scope.REQUEST)
    def create_user_handler(
        self,
        users_repository: IUsersRepository,
        hasher: IPwdHasher,
        transaction_manager: ITransactionManager,
        email_validator: IEmailValidatorService,
        email_notifications: IEmailNotificationsService,
    ) -> CreateUserHandler:
        return CreateUserHandler(
            users_repository,
            hasher,
            transaction_manager,
            email_validator,
            email_notifications,
        )

    @provide(scope=Scope.REQUEST)
    def get_user_handler(
        self,
        users_repository: IUsersRepository,
        transaction_manager: ITransactionManager,
    ) -> GetUserHandler:
        return GetUserHandler(users_repository, transaction_manager)

    @provide(scope=Scope.REQUEST)
    def update_user_handler(
        self,
        users_repository: IUsersRepository,
        hasher: IPwdHasher,
        transaction_manager: ITransactionManager,
        email_validator: IEmailValidatorService,
        email_notifications: IEmailNotificationsService,
    ) -> UpdateUserHandler:
        return UpdateUserHandler(
            users_repository,
            hasher,
            transaction_manager,
            email_validator,
            email_notifications,
        )

    @provide(scope=Scope.REQUEST)
    def delete_user_handler(
        self,
        users_repository: IUsersRepository,
        hasher: IPwdHasher,
        transaction_manager: ITransactionManager,
        email_notifications: IEmailNotificationsService,
    ) -> DeleteUserHandler:
        return DeleteUserHandler(
            users_repository, hasher, transaction_manager, email_notifications
        )


class AuthFeaturesProvider(Provider):
    def __init__(self, jwt_settings: JWTSettings, scope=None, component=None):
        super().__init__(scope, component)
        self._jwt_settings = jwt_settings

    @provide(scope=Scope.REQUEST)
    def jwt_token_service(self) -> ITokenJWTService:
        return TokenJWTService(self._jwt_settings)

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
            users_repository,
            hasher,
            token_service,
            refresh_token_repository,
            transaction_manager,
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
            users_repository,
            refresh_token_repository,
            token_service,
            transaction_manager,
        )


class ServicesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def rate_limiter_service(
        self, repository: IRateLimiterCacheRepository
    ) -> IRateLimiterService:
        return RateLimiterService(repository)

    @provide(scope=Scope.REQUEST)
    def email_notifications_service(
        self,
        producer: IEmailNotificationsProducer,
        sender: IEmailSender,
        smtp_settings: SMTPSettings,
    ) -> IEmailNotificationsService:
        return EmailNotificationsService(producer, sender, smtp_settings.sender)
