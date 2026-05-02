from dataclasses import dataclass

import aiosmtplib


@dataclass
class TEmailMessage:
    recipient: str
    subject: str
    content: str


class IEmailNotificationsService:
    async def enqueue(self, message: TEmailMessage) -> None: ...

    async def send(
        self, message: TEmailMessage
    ) -> tuple[dict[str, aiosmtplib.SMTPResponse], str]: ...
