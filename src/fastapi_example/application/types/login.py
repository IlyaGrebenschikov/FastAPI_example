from dataclasses import dataclass

@dataclass
class LoginCredentials:
    username: str
    password: str
    scopes: list[str] = None
