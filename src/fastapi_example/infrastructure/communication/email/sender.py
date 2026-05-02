import aiosmtplib
from email.message import EmailMessage

from fastapi_example.application.interfaces.communication import TEmailMessage, IEmailSender


class EmailSender(IEmailSender):
    def __init__(self, client: aiosmtplib.SMTP, from_email: str):
        self._client = client
        self._from_email = from_email

    async def send(self, message: TEmailMessage) -> tuple[dict[str, aiosmtplib.SMTPResponse], str]:
        email_message = self._build_message(message)
        return await self._client.send_message(email_message)

    def _build_message(self, message: TEmailMessage) -> EmailMessage:
        email_message = EmailMessage()
        email_message["From"] = self._from_email
        email_message["To"] = message.recipient
        email_message["Subject"] = message.subject
        email_message.set_content(message.content)
        return email_message
