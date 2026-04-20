from typing import Protocol


class IEmailValidatorService(Protocol):
    async def validate(self, email: str) -> None: ...
