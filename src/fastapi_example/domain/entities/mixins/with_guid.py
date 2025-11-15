from dataclasses import dataclass
from uuid import UUID

@dataclass
class UUIDMixin:
    id: UUID
