from typing import Protocol

class ITokenService(Protocol):
    async def get_user_id_from_token(self, token: str) -> str: ...
