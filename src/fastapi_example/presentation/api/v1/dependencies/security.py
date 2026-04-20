from typing import Annotated

from fastapi import Security
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token/access")


async def get_bearer_token(token: Annotated[str, Security(oauth2_scheme)]) -> str:
    return token
