import aiosmtplib
from email.message import EmailMessage

from fastapi_example.application.interfaces.communication import IEmailSender


class EmailSender(IEmailSender):
    def __init__(self, client: aiosmtplib.SMTP, from_email: str):
        self._client = client
        self._from_email = from_email

    async def send(self, message: EmailMessage) -> tuple[dict[str, aiosmtplib.SMTPResponse], str]:
        return await self._client.send_message(message)
