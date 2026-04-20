from dishka import Provider, Scope, provide

from fastapi_example.application.interfaces.services import (
    ITokenJWTService,
)
from fastapi_example.application.services import TokenJWTService
from fastapi_example.infrastructure.settings import JWTSettings


class AuthServiceProvider(Provider):
    def __init__(self, settings: JWTSettings, scope=None, component=None):
        super().__init__(scope, component)
        self._settings = settings

    @provide(scope=Scope.REQUEST)
    def jwt_token(self) -> ITokenJWTService:
        return TokenJWTService(self._settings)
