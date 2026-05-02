import aiosmtplib
from email.message import EmailMessage

from fastapi_example.application.interfaces.communication import IEmailSender


class EmailSender(IEmailSender):
    def __init__(self, client: aiosmtplib.SMTP):
        self._client = client

    async def send_email(
        self, message: EmailMessage
    ) -> tuple[dict[str, aiosmtplib.SMTPResponse], str]:
        return await self._client.send_message(message)
