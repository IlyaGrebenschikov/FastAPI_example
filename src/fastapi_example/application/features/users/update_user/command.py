from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class UpdateUserCommand:
    user_id: UUID
    username: Optional[str] = None
    email: Optional[str] = None
