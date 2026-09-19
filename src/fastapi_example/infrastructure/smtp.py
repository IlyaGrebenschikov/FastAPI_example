from email.message import EmailMessage

import aiosmtplib

from fastapi_example.application.interfaces import IEmailSender
from fastapi_example.core.settings import SMTPSettings


def create_smtp_client(settings: SMTPSettings) -> aiosmtplib.SMTP:
    return aiosmtplib.SMTP(
        hostname=settings.host, port=settings.port, use_tls=settings.use_tls
    )


class EmailSender(IEmailSender):
    def __init__(self, client: aiosmtplib.SMTP) -> None:
        self._client = client

    async def send_email(
        self, message: EmailMessage
    ) -> tuple[dict[str, aiosmtplib.SMTPResponse], str]:
        return await self._client.send_message(message)
