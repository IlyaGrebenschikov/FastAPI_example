from dataclasses import dataclass


@dataclass
class EmailVerificationResult:
    is_valid_format: bool
    is_deliverable: bool
    is_disposable: bool
    details: str | None = None


class IEmailVerifier:
    async def check(self, email: str) -> EmailVerificationResult: ...
