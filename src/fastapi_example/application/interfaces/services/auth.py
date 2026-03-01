from typing import Protocol

from fastapi_example.application.dto import Token
from fastapi_example.application.types import LoginCredentials

class IAuthService(Protocol):
    async def login(self, credentials: LoginCredentials) -> Token: ...
