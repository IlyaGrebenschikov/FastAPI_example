from dishka import Provider, Scope, provide

from fastapi_example.application.interfaces.http_clients import IEmailVerifier
from fastapi_example.infrastructure.http_clients import (
    AbstractApiEmailVerifier,
    NullEmailVerifier,
)
from fastapi_example.infrastructure.settings import EmailVerifierSettings


class HTTPClientsProvider(Provider):
    def __init__(
        self, email_verifier_settings: EmailVerifierSettings, scope=None, component=None
    ):
        self._email_verifier_settings = email_verifier_settings
        super().__init__(scope, component)

    @provide(scope=Scope.APP)
    def email_verifier(self) -> IEmailVerifier:
        if not self._email_verifier_settings.enabled:
            return NullEmailVerifier()
        return AbstractApiEmailVerifier(self._email_verifier_settings.api_key)
