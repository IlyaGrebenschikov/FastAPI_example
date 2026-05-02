from dataclasses import dataclass
from typing import Protocol

import aiosmtplib


@dataclass
class TEmailMessage:
    recipient: str
    subject: str
    content: str


class IEmailSender(Protocol):
    async def send_email(self, message: TEmailMessage) -> tuple[dict[str, aiosmtplib.SMTPResponse], str]: ...
