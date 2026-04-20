from unittest.mock import AsyncMock, MagicMock

import pytest

from fastapi_example.infrastructure.settings import JWTSettings


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
