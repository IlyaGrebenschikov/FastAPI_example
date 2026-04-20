from dataclasses import dataclass
from typing import TypedDict, NotRequired, Optional

from .base import BaseSchema


class Token(BaseSchema):
    access_token: str
    token_type: str


@dataclass
class LoginCredentials:
    username: str
    password: str
    scopes: Optional[list[str]] = None
