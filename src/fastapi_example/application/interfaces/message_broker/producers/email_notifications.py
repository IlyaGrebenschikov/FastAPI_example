from typing import Protocol

from fastapi_example.application.interfaces.services import TEmailMessage


class IEmailNotificationsProducer(Protocol):
    async def publish(self, message: TEmailMessage) -> None: ...
