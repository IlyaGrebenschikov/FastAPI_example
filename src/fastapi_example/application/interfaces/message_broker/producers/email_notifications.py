from typing import TypedDict

class TEmailMessage(TypedDict):
    recipient: str
    subject: str
    content: str


class IEmailNotificationsProducer:
    async def publish(self, message: TEmailMessage) -> None: ...
