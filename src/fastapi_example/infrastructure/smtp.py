from email.message import EmailMessage

import aiosmtplib

from fastapi_example.application.interfaces import IEmailSender
from fastapi_example.core.settings import SMTPSettings


def create_smtp_client(settings: SMTPSettings) -> aiosmtplib.SMTP:
    return aiosmtplib.SMTP(
        hostname=settings.host,
        port=settings.port,
        use_tls=settings.use_tls,
        start_tls=False,
    )


class EmailSender(IEmailSender):
    def __init__(self, client: aiosmtplib.SMTP) -> None:
        self._client = client

    async def send_email(self, message: EmailMessage) -> None:
        await self._client.send_message(message)
