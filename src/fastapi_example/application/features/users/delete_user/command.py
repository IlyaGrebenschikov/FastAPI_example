from dataclasses import dataclass
from uuid import UUID


@dataclass
class DeleteUserCommand:
    user_id: UUID
    password: str
