import json
import logging
import httpx

from fastapi_example.application.interfaces.http_clients import EmailVerificationResult, IEmailVerifier

log = logging.getLogger(__name__)


class AbstractApiEmailVerifier(IEmailVerifier):
    __doc__ = "API url - https://docs.abstractapi.com/api/email-reputation"

    def __init__(self, api_key: str):
        self._client = httpx.AsyncClient(timeout=5.0)
        self._key = api_key

    async def check(self, email: str) -> EmailVerificationResult:
        try:
            r = await self._client.get(
                "https://emailvalidation.abstractapi.com/v1/",
                params={"api_key": self._key, "email": email},
            )
            r.raise_for_status()
            js = r.json()
        except httpx.TimeoutException:
            log.warning("AbstractAPI timeout for email=%s", email)
            return EmailVerificationResult(is_valid_format=True, is_deliverable=False, is_disposable=False, details="transient_timeout")
        except httpx.HTTPStatusError as e:
            log.error("AbstractAPI HTTP error %s for email=%s: %s", e.response.status_code, email, e)
            return EmailVerificationResult(is_valid_format=True, is_deliverable=False, is_disposable=False, details=f"http_{e.response.status_code}")
        except httpx.RequestError as e:
            log.error("AbstractAPI request error for email=%s: %s", email, e)
            return EmailVerificationResult(is_valid_format=True, is_deliverable=False, is_disposable=False, details="network_error")
        except (ValueError, json.JSONDecodeError):
            log.exception("Invalid JSON from AbstractAPI for email=%s", email)
            return EmailVerificationResult(is_valid_format=True, is_deliverable=False, is_disposable=False, details="invalid_response")

        is_format = js.get("is_format_valid")
        if is_format is None:
            is_format = js.get("email_deliverability", {}).get("is_format_valid", True)

        return EmailVerificationResult(
            is_valid_format=bool(is_format),
            is_deliverable=js.get("email_deliverability", {}).get("status") == "deliverable",
            is_disposable=js.get("is_disposable", False),
            details=js.get("email_deliverability", {}).get("status_detail"),
        )
