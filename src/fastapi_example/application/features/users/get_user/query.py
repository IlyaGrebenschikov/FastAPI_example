from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class GetUserQuery:
    user_id: Optional[UUID]
