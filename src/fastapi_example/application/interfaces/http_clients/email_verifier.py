from dataclasses import dataclass
from typing import Protocol


@dataclass
class EmailVerificationResult:
    is_valid_format: bool
    is_deliverable: bool
    is_disposable: bool
    details: str | None = None


class IEmailVerifier(Protocol):
    async def check(self, email: str) -> EmailVerificationResult: ...
