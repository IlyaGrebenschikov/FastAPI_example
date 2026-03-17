from typing import Protocol
from uuid import UUID


class ITokenService(Protocol):
    async def get_user_id_from_token(self, token: str) -> UUID: ...
