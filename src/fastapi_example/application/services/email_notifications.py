import logging
from email.message import EmailMessage

from fastapi_example.application.interfaces import IEmailSender
from fastapi_example.application.interfaces.message_broker.producers import (
    IEmailNotificationsProducer,
)
from fastapi_example.application.interfaces.services import (
    IEmailNotificationsService,
    TEmailMessage,
)

log = logging.getLogger(__name__)


class EmailNotificationsService(IEmailNotificationsService):
    def __init__(
        self,
        producer: IEmailNotificationsProducer,
        sender: IEmailSender,
        email_sender: str,
    ) -> None:
        self._producer = producer
        self._sender = sender
        self._email_sender = email_sender

    async def enqueue(self, message: TEmailMessage) -> None:
        log.info("enqueue: to=%s subject=%s", message.recipient, message.subject)
        await self._producer.publish(message=message)

    async def send(self, message: TEmailMessage) -> None:
        log.info("send: to=%s subject=%s", message.recipient, message.subject)
        await self._sender.send_email(message=self._build_message(message))

    def _build_message(self, message: TEmailMessage) -> EmailMessage:
        email_message = EmailMessage()
        email_message["From"] = self._email_sender
        email_message["To"] = message.recipient
        email_message["Subject"] = message.subject
        email_message.set_content(message.content)
        return email_message
