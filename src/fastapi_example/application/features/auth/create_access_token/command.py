from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateAccessTokenCommand:
    username: str
    password: str
    scopes: Optional[list[str]] = None
