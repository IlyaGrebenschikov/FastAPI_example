from dataclasses import dataclass


@dataclass
class CreateUserCommand:
    username: str
    email: str
    password: str
