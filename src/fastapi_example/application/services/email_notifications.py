import logging
from dataclasses import asdict
from email.message import EmailMessage

import aiosmtplib

from fastapi_example.application.interfaces.communication import IEmailSender
from fastapi_example.application.interfaces.message_broker.producers import (
    IEmailNotificationsProducer,
    TEmailMessage as TPubEmailMessage
)
from fastapi_example.application.interfaces.services import IEmailNotificationsService, TEmailMessage
from fastapi_example.application.settings import EmailNotificationSettings

log = logging.getLogger(__name__)


class EmailNotificationsService(IEmailNotificationsService):
    def __init__(self, producer: IEmailNotificationsProducer, sender: IEmailSender, settings: EmailNotificationSettings):
        self._producer = producer
        self._sender = sender
        self._settings = settings

    async def enqueue(self, message: TEmailMessage) -> None:
        log.info(f"enqueue: {message}")
        await self._producer.publish(message=TPubEmailMessage(**asdict(message)))

    async def send(self, message: TEmailMessage) -> tuple[dict[str, aiosmtplib.SMTPResponse], str]:
        log.info(f"send: {message}")
        return await self._sender.send_email(message=self._build_message(message))

    def _build_message(self, message: TEmailMessage) -> EmailMessage:
        email_message = EmailMessage()
        email_message["From"] = self._settings.sender
        email_message["To"] = message.recipient
        email_message["Subject"] = message.subject
        email_message.set_content(message.content)
        return email_message