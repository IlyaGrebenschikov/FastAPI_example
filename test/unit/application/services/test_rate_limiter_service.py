import pytest
from unittest.mock import AsyncMock

from fastapi_example.application.exceptions.http_exceptions import (
    TooManyRequestsError,
)
from fastapi_example.application.services.rate_limiter import RateLimiterService


class TestRateLimiterService:
    @pytest.fixture
    def rate_limiter_service(self, mock_cache_repository):
        return RateLimiterService(mock_cache_repository)

    @pytest.mark.asyncio
    async def test_check_within_limit(
        self, rate_limiter_service: RateLimiterService, mock_cache_repository
    ):
        mock_cache_repository.get_request_count = AsyncMock(return_value=3)

        await rate_limiter_service.check(
            identifier="user123",
            path="/api/test",
            limit=5,
            window=60,
        )

    @pytest.mark.asyncio
    async def test_check_at_limit(
        self, rate_limiter_service: RateLimiterService, mock_cache_repository
    ):
        mock_cache_repository.get_request_count = AsyncMock(return_value=5)

        await rate_limiter_service.check(
            identifier="user123",
            path="/api/test",
            limit=5,
            window=60,
        )

    @pytest.mark.asyncio
    async def test_check_exceeds_limit(
        self, rate_limiter_service: RateLimiterService, mock_cache_repository
    ):
        mock_cache_repository.get_request_count = AsyncMock(return_value=6)

        with pytest.raises(TooManyRequestsError):
            await rate_limiter_service.check(
                identifier="user123",
                path="/api/test",
                limit=5,
                window=60,
            )

    @pytest.mark.asyncio
    async def test_check_zero_requests(
        self, rate_limiter_service: RateLimiterService, mock_cache_repository
    ):
        mock_cache_repository.get_request_count = AsyncMock(return_value=0)

        await rate_limiter_service.check(
            identifier="user123",
            path="/api/test",
            limit=5,
            window=60,
        )

    @pytest.mark.asyncio
    async def test_check_creates_correct_key(
        self, rate_limiter_service: RateLimiterService, mock_cache_repository
    ):
        mock_cache_repository.get_request_count = AsyncMock(return_value=1)

        identifier = "user456"
        path = "/api/users"

        await rate_limiter_service.check(
            identifier=identifier,
            path=path,
            limit=10,
            window=120,
        )

        mock_cache_repository.get_request_count.assert_called_once()
        args = mock_cache_repository.get_request_count.call_args
        assert args[0][0] == f"rl:{identifier}:{path}"
