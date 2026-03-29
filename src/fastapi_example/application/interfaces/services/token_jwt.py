from typing import Protocol
from uuid import UUID

from fastapi_example.application.dto import TokenPayload, TokenDecoded


class ITokenJWTService(Protocol):
    def create_access_token(self, data: TokenPayload) -> str: ...

    def _verify_token(self, token: str) -> TokenDecoded: ...

    def get_user_id_from_token(self, token: str) -> UUID: ...
