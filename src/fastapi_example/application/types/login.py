from dataclasses import dataclass
from typing import Optional

@dataclass
class LoginCredentials:
    username: str
    password: str
    scopes: Optional[list[str]] = None
