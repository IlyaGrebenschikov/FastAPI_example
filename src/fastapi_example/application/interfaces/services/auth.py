from dataclasses import dataclass
from typing import Optional, Protocol

from fastapi_example.application.dto import Token


@dataclass
class LoginCredentials:
    username: str
    password: str
    scopes: Optional[list[str]] = None


class IAuthService(Protocol):
    async def login(self, credentials: LoginCredentials) -> Token: ...
