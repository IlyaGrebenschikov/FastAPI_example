from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from fastapi_example.application.http_exceptions import UnAuthorizedError
from fastapi_example.application.interfaces.services import ITokenJWTService, TokenData

access_token_bearer_scheme = HTTPBearer(auto_error=False, scheme_name="Access token")
refresh_token_bearer_scheme = HTTPBearer(auto_error=False, scheme_name="Refresh token")


def _extract_token(credentials: HTTPAuthorizationCredentials | None) -> str:
    if credentials is None:
        raise UnAuthorizedError("Missing bearer token")
    return credentials.credentials


@inject
def get_current_user_id_from_access_token(
    token_service: FromDishka[ITokenJWTService],
    credentials: HTTPAuthorizationCredentials | None = Security(  # noqa: B008
        access_token_bearer_scheme
    ),
) -> UUID:
    return token_service.verify_access_token(_extract_token(credentials))


@inject
def get_refresh_token_data(
    token_service: FromDishka[ITokenJWTService],
    credentials: HTTPAuthorizationCredentials | None = Security(  # noqa: B008
        refresh_token_bearer_scheme
    ),
) -> TokenData:
    return token_service.verify_refresh_token(_extract_token(credentials))
