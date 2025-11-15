from dataclasses import dataclass
from datetime import datetime

@dataclass
class TimestampMixin:
    created_at: datetime
    updated_at: datetime
