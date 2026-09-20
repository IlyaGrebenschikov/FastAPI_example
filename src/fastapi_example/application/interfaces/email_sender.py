from email.message import EmailMessage
from typing import Protocol


class IEmailSender(Protocol):
    async def send_email(self, message: EmailMessage) -> None: ...
