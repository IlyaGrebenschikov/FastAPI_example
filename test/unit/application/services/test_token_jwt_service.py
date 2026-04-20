from uuid import uuid4

import jwt
import pytest

from fastapi_example.application.exceptions.http_exceptions import (
    UnAuthorizedError,
)
from fastapi_example.application.services.token_jwt import TokenJWTService
from fastapi_example.infrastructure.settings import JWTSettings


class TestTokenJWTService:
    @pytest.fixture
    def token_service(self, jwt_settings: JWTSettings) -> TokenJWTService:
        return TokenJWTService(jwt_settings)

    def test_create_access_token_success(self, token_service: TokenJWTService):
        payload = {"sub": str(uuid4())}
        token = token_service.create_access_token(payload)

        assert isinstance(token, str)
        assert len(token) > 0
        decoded = jwt.decode(
            token,
            token_service._settings.public_key,
            algorithms=[token_service._settings.algorithm],
        )
        assert decoded["sub"] == payload["sub"]
        assert "exp" in decoded
        assert "iat" in decoded

    def test_create_access_token_with_scopes(self, token_service: TokenJWTService):
        user_id = str(uuid4())
        payload = {"sub": user_id, "scopes": ["read", "write"]}
        token = token_service.create_access_token(payload)

        decoded = jwt.decode(
            token,
            token_service._settings.public_key,
            algorithms=[token_service._settings.algorithm],
        )
        assert decoded["sub"] == user_id
        assert decoded["scopes"] == ["read", "write"]

    def test_verify_token_success(self, token_service: TokenJWTService):
        user_id = str(uuid4())
        payload = {"sub": user_id}
        token = token_service.create_access_token(payload)

        decoded = token_service._verify_token(token)
        assert decoded["sub"] == user_id

    def test_verify_token_invalid(self, token_service: TokenJWTService):
        with pytest.raises(UnAuthorizedError):
            token_service._verify_token("invalid.token.here")

    def test_verify_token_expired(self, jwt_settings: JWTSettings):
        expired_settings = JWTSettings(
            algorithm="RS256",
            expiration=-1,
        )
        service = TokenJWTService(expired_settings)
        payload = {"sub": str(uuid4())}
        token = service.create_access_token(payload)

        with pytest.raises(UnAuthorizedError, match="Token expired"):
            service._verify_token(token)

    def test_verify_token_missing_subject(self, jwt_settings: JWTSettings):
        service = TokenJWTService(jwt_settings)
        payload = {"data": "test"}
        token = jwt.encode(
            payload,
            jwt_settings.private_key,
            algorithm=jwt_settings.algorithm,
        )

        with pytest.raises(UnAuthorizedError, match="Token missing subject"):
            service._verify_token(token)

    def test_get_user_id_from_token_success(self, token_service: TokenJWTService):
        user_id = uuid4()
        payload = {"sub": str(user_id)}
        token = token_service.create_access_token(payload)

        result = token_service.get_user_id_from_token(token)
        assert result == user_id

    def test_get_user_id_from_token_invalid(self, token_service: TokenJWTService):
        with pytest.raises(UnAuthorizedError):
            token_service.get_user_id_from_token("invalid.token.here")

    def test_get_user_id_from_token_invalid_uuid_format(
        self, token_service: TokenJWTService
    ):
        payload = {"sub": "not-a-uuid"}
        token = token_service.create_access_token(payload)

        with pytest.raises(ValueError):
            token_service.get_user_id_from_token(token)
