from dishka import (
    Provider,
    Scope,
    provide
)
from pwdlib import PasswordHash

from fastapi_example.application.interfaces.services import IHasherService
from fastapi_example.application.services import Argon2HasherService

class HasherServiceProvider(Provider):
    def __init__(self, scope=None, component=None):
        super().__init__(scope, component)

    @provide(scope=Scope.APP)
    def get_password_hash(self) -> PasswordHash:
        return PasswordHash.recommended()

    @provide(scope=Scope.APP)
    def argon2_hasher(self, hasher: PasswordHash) -> IHasherService:
        return Argon2HasherService(hasher)
