from dishka import (
    Provider,
    Scope,
    provide
)
from pwdlib import PasswordHash

from fastapi_example.application.interfaces.security import IHasher
from fastapi_example.infrastructure.security import Argon2Hasher

class HasherProvider(Provider):
    def __init__(self, scope=None, component=None):
        super().__init__(scope, component)

    @provide(scope=Scope.APP)
    def get_password_hash(self) -> PasswordHash:
        return PasswordHash.recommended()

    @provide(scope=Scope.APP)
    def argon2_hasher(self, hasher: PasswordHash) -> IHasher:
        return Argon2Hasher(hasher)
