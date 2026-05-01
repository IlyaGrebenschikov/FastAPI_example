import logging

from fastapi_example.application.interfaces.http_clients import IEmailVerifier
from fastapi_example.application.exceptions.http_exceptions import (
    BadRequestError,
    ServiceUnavailableError,
)

log = logging.getLogger(__name__)


class EmailValidatorService:
    def __init__(self, email_verifier: IEmailVerifier) -> None:
        self._email_verifier = email_verifier

    async def validate(self, email: str) -> None:
        ver = await self._email_verifier.check(email)
        if ver.details and ver.details.startswith("http_401"):
            log.error("Email verifier unauthorized (401) for email=%s", email)
            raise ServiceUnavailableError("Email verification service unauthorized")
        if ver.details and ver.details.startswith(("transient", "network", "http_5")):
            raise ServiceUnavailableError("Email verification service unavailable")
        if not ver.is_valid_format:
            raise BadRequestError(f"Invalid email format: {email}")
        if not ver.is_deliverable:
            raise BadRequestError("Email appears undeliverable")
        if ver.is_disposable:
            raise BadRequestError("Disposable email addresses are not allowed")
