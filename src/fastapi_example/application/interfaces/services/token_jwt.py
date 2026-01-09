from typing import Protocol

from fastapi_example.application.types import TokenDecoded, TokenPayload

class ITokenJWTService(Protocol):
    def create_access_token(self, data: TokenPayload) -> str: ...

    def verify_token(self, token: str) -> TokenDecoded: ...
