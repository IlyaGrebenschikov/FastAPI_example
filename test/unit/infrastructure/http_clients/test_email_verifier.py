from unittest.mock import AsyncMock, MagicMock, patch
import json

import pytest
import httpx

from fastapi_example.infrastructure.http_clients import AbstractApiEmailVerifier


class TestAbstractApiEmailVerifier:
    @pytest.fixture
    def email_verifier(self) -> AbstractApiEmailVerifier:
        return AbstractApiEmailVerifier(api_key="test_api_key")

    @pytest.mark.asyncio
    async def test_check_valid_deliverable_email(
        self, email_verifier: AbstractApiEmailVerifier
    ):
        """Test successful verification of a valid, deliverable email."""
        email = "user@example.com"
        mock_response = {
            "is_format_valid": True,
            "email_deliverability": {
                "status": "deliverable",
                "status_detail": "ok",
                "is_format_valid": True,
            },
            "is_disposable": False,
        }

        with patch.object(email_verifier._client, "get") as mock_get:
            mock_response_obj = MagicMock()
            mock_response_obj.json.return_value = mock_response
            mock_response_obj.raise_for_status = MagicMock()
            mock_get.return_value = mock_response_obj

            result = await email_verifier.check(email)

            assert result.is_valid_format is True
            assert result.is_deliverable is True
            assert result.is_disposable is False
            assert result.details == "ok"
            mock_get.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_invalid_format_email(
        self, email_verifier: AbstractApiEmailVerifier
    ):
        """Test verification of an email with invalid format."""
        email = "invalid-email"
        mock_response = {
            "is_format_valid": False,
            "email_deliverability": {
                "status": "undeliverable",
                "status_detail": "invalid_format",
                "is_format_valid": False,
            },
            "is_disposable": False,
        }

        with patch.object(email_verifier._client, "get") as mock_get:
            mock_response_obj = MagicMock()
            mock_response_obj.json.return_value = mock_response
            mock_response_obj.raise_for_status = MagicMock()
            mock_get.return_value = mock_response_obj

            result = await email_verifier.check(email)

            assert result.is_valid_format is False
            assert result.is_deliverable is False
            assert result.is_disposable is False

    @pytest.mark.asyncio
    async def test_check_disposable_email(
        self, email_verifier: AbstractApiEmailVerifier
    ):
        """Test verification of a disposable email address."""
        email = "user@10minutemail.com"
        mock_response = {
            "is_format_valid": True,
            "email_deliverability": {
                "status": "deliverable",
                "status_detail": "ok",
                "is_format_valid": True,
            },
            "is_disposable": True,
        }

        with patch.object(email_verifier._client, "get") as mock_get:
            mock_response_obj = MagicMock()
            mock_response_obj.json.return_value = mock_response
            mock_response_obj.raise_for_status = MagicMock()
            mock_get.return_value = mock_response_obj

            result = await email_verifier.check(email)

            assert result.is_valid_format is True
            assert result.is_deliverable is True
            assert result.is_disposable is True

    @pytest.mark.asyncio
    async def test_check_undeliverable_email(
        self, email_verifier: AbstractApiEmailVerifier
    ):
        """Test verification of an undeliverable email."""
        email = "nonexistent@example.com"
        mock_response = {
            "is_format_valid": True,
            "email_deliverability": {
                "status": "undeliverable",
                "status_detail": "mailbox_does_not_exist",
                "is_format_valid": True,
            },
            "is_disposable": False,
        }

        with patch.object(email_verifier._client, "get") as mock_get:
            mock_response_obj = MagicMock()
            mock_response_obj.json.return_value = mock_response
            mock_response_obj.raise_for_status = MagicMock()
            mock_get.return_value = mock_response_obj

            result = await email_verifier.check(email)

            assert result.is_valid_format is True
            assert result.is_deliverable is False
            assert result.is_disposable is False
            assert result.details == "mailbox_does_not_exist"

    @pytest.mark.asyncio
    async def test_check_timeout_exception(
        self, email_verifier: AbstractApiEmailVerifier
    ):
        """Test handling of timeout exception."""
        email = "user@example.com"

        with patch.object(email_verifier._client, "get") as mock_get:
            mock_get.side_effect = httpx.TimeoutException("Request timeout")

            result = await email_verifier.check(email)

            assert result.is_valid_format is True
            assert result.is_deliverable is False
            assert result.is_disposable is False
            assert result.details == "transient_timeout"

    @pytest.mark.asyncio
    async def test_check_http_401_error(self, email_verifier: AbstractApiEmailVerifier):
        """Test handling of HTTP 401 (Unauthorized) error."""
        email = "user@example.com"

        with patch.object(email_verifier._client, "get") as mock_get:
            mock_response_obj = MagicMock()
            mock_response_obj.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Unauthorized",
                request=MagicMock(),
                response=MagicMock(status_code=401),
            )
            mock_get.return_value = mock_response_obj

            result = await email_verifier.check(email)

            assert result.is_valid_format is True
            assert result.is_deliverable is False
            assert result.is_disposable is False
            assert result.details == "http_401"

    @pytest.mark.asyncio
    async def test_check_http_500_error(self, email_verifier: AbstractApiEmailVerifier):
        """Test handling of HTTP 500 (Server Error)."""
        email = "user@example.com"

        with patch.object(email_verifier._client, "get") as mock_get:
            mock_response_obj = MagicMock()
            mock_response_obj.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Server Error",
                request=MagicMock(),
                response=MagicMock(status_code=500),
            )
            mock_get.return_value = mock_response_obj

            result = await email_verifier.check(email)

            assert result.is_valid_format is True
            assert result.is_deliverable is False
            assert result.is_disposable is False
            assert result.details == "http_500"

    @pytest.mark.asyncio
    async def test_check_http_502_error(self, email_verifier: AbstractApiEmailVerifier):
        """Test handling of HTTP 502 (Bad Gateway)."""
        email = "user@example.com"

        with patch.object(email_verifier._client, "get") as mock_get:
            mock_response_obj = MagicMock()
            mock_response_obj.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Bad Gateway",
                request=MagicMock(),
                response=MagicMock(status_code=502),
            )
            mock_get.return_value = mock_response_obj

            result = await email_verifier.check(email)

            assert result.is_valid_format is True
            assert result.is_deliverable is False
            assert result.is_disposable is False
            assert result.details == "http_502"

    @pytest.mark.asyncio
    async def test_check_request_error(self, email_verifier: AbstractApiEmailVerifier):
        """Test handling of network request error."""
        email = "user@example.com"

        with patch.object(email_verifier._client, "get") as mock_get:
            mock_get.side_effect = httpx.RequestError("Network error")

            result = await email_verifier.check(email)

            assert result.is_valid_format is True
            assert result.is_deliverable is False
            assert result.is_disposable is False
            assert result.details == "network_error"

    @pytest.mark.asyncio
    async def test_check_json_decode_error(
        self, email_verifier: AbstractApiEmailVerifier
    ):
        """Test handling of JSON decode error."""
        email = "user@example.com"

        with patch.object(email_verifier._client, "get") as mock_get:
            mock_response_obj = MagicMock()
            mock_response_obj.raise_for_status = MagicMock()
            mock_response_obj.json.side_effect = json.JSONDecodeError(
                "Invalid JSON", "", 0
            )
            mock_get.return_value = mock_response_obj

            result = await email_verifier.check(email)

            assert result.is_valid_format is True
            assert result.is_deliverable is False
            assert result.is_disposable is False
            assert result.details == "invalid_response"

    @pytest.mark.asyncio
    async def test_check_response_missing_format_valid_uses_fallback(
        self, email_verifier: AbstractApiEmailVerifier
    ):
        """Test fallback to email_deliverability.is_format_valid when top-level is missing."""
        email = "user@example.com"
        mock_response = {
            "email_deliverability": {
                "status": "deliverable",
                "status_detail": "ok",
                "is_format_valid": True,
            },
            "is_disposable": False,
        }

        with patch.object(email_verifier._client, "get") as mock_get:
            mock_response_obj = MagicMock()
            mock_response_obj.json.return_value = mock_response
            mock_response_obj.raise_for_status = MagicMock()
            mock_get.return_value = mock_response_obj

            result = await email_verifier.check(email)

            assert result.is_valid_format is True
            assert result.is_deliverable is True

    @pytest.mark.asyncio
    async def test_check_response_default_is_format_valid_true(
        self, email_verifier: AbstractApiEmailVerifier
    ):
        """Test default is_format_valid to True when not present."""
        email = "user@example.com"
        mock_response = {
            "email_deliverability": {
                "status": "deliverable",
                "status_detail": "ok",
            },
            "is_disposable": False,
        }

        with patch.object(email_verifier._client, "get") as mock_get:
            mock_response_obj = MagicMock()
            mock_response_obj.json.return_value = mock_response
            mock_response_obj.raise_for_status = MagicMock()
            mock_get.return_value = mock_response_obj

            result = await email_verifier.check(email)

            assert result.is_valid_format is True
            assert result.is_deliverable is True

    @pytest.mark.asyncio
    async def test_check_calls_api_with_correct_params(
        self, email_verifier: AbstractApiEmailVerifier
    ):
        """Test that API is called with correct email and API key parameters."""
        email = "user@example.com"
        mock_response = {
            "is_format_valid": True,
            "email_deliverability": {
                "status": "deliverable",
                "status_detail": "ok",
            },
            "is_disposable": False,
        }

        with patch.object(email_verifier._client, "get") as mock_get:
            mock_response_obj = MagicMock()
            mock_response_obj.json.return_value = mock_response
            mock_response_obj.raise_for_status = MagicMock()
            mock_get.return_value = mock_response_obj

            await email_verifier.check(email)

            mock_get.assert_called_once_with(
                "https://emailreputation.abstractapi.com/v1/",
                params={"api_key": "test_api_key", "email": email},
            )
