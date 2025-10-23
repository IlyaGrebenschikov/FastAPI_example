from dataclasses import dataclass

from mixins import TimestampMixin, UUIDMixin

@dataclass
class User(UUIDMixin, TimestampMixin):
    username: str
    email: str
    password: str
