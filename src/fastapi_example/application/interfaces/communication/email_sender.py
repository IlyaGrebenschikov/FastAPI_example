from email.message import EmailMessage
from typing import Protocol

import aiosmtplib


class IEmailSender(Protocol):
    async def send_email(
        self, message: EmailMessage
    ) -> tuple[dict[str, aiosmtplib.SMTPResponse], str]: ...
