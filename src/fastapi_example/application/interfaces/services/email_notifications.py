from dataclasses import dataclass
from typing import Protocol


@dataclass
class TEmailMessage:
    recipient: str
    subject: str
    content: str


class IEmailNotificationsService(Protocol):
    async def enqueue(self, message: TEmailMessage) -> None: ...

    async def send(self, message: TEmailMessage) -> None: ...
