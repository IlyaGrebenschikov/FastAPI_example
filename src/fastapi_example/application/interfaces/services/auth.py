from dataclasses import dataclass
from typing import Optional, Protocol

from fastapi_example.application.dto import Token, LoginCredentials


class IAuthService(Protocol):
    async def login(self, credentials: LoginCredentials) -> Token: ...
