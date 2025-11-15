from typing import Protocol

from fastapi.security import OAuth2PasswordRequestForm

from fastapi_example.application.dto import Token

class IAuthService(Protocol):
    async def login(self, query: OAuth2PasswordRequestForm) -> Token: ...

    def get_sub_from_token(self, token: str) -> str: ...
