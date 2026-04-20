from dishka import Provider, Scope, provide

from fastapi_example.application.interfaces.services import IEmailValidatorService
from fastapi_example.application.services import EmailValidatorService
from fastapi_example.application.interfaces.http_clients import IEmailVerifier


class EmailValidatorServiceProvider(Provider):
    def __init__(self, scope=None, component=None):
        super().__init__(scope, component)

    @provide(scope=Scope.REQUEST)
    def email_validator(self, email_verifier: IEmailVerifier) -> IEmailValidatorService:
        return EmailValidatorService(email_verifier)
