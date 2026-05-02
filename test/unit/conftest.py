from unittest.mock import AsyncMock, MagicMock

import pytest

from fastapi_example.infrastructure.settings import JWTSettings
from fastapi_example.application.interfaces.http_clients import EmailVerificationResult


@pytest.fixture
def jwt_settings() -> JWTSettings:
    return JWTSettings(
        algorithm="RS256",
        expiration=30,
    )


@pytest.fixture
def mock_transaction_manager():
    mock = MagicMock()
    mock.__aenter__ = AsyncMock(return_value=mock)
    mock.__aexit__ = AsyncMock(return_value=None)
    return mock


@pytest.fixture
def mock_users_repository():
    return AsyncMock()


@pytest.fixture
def mock_cache_repository():
    return AsyncMock()


@pytest.fixture
def mock_hasher():
    mock = MagicMock()
    mock.hash_password = MagicMock(return_value="hashed_password")
    mock.verify_password = MagicMock(return_value=True)
    return mock


@pytest.fixture
def mock_email_verifier():
    mock = AsyncMock()
    mock.check = AsyncMock(
        return_value=EmailVerificationResult(
            is_valid_format=True,
            is_deliverable=True,
            is_disposable=False,
            details="ok",
        )
    )
    return mock


@pytest.fixture
def mock_email_notifications():
    mock = AsyncMock()
    mock.enqueue = AsyncMock(return_value=None)
    return mock
