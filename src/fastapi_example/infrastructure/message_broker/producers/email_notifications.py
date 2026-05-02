from dataclasses import asdict

from faststream.kafka import KafkaBroker

from fastapi_example.application.interfaces.communication import TEmailMessage
from fastapi_example.application.interfaces.message_broker.producers import IEmailNotificationsProducer


class EmailNotificationsProducer(IEmailNotificationsProducer):
    def __init__(self, broker: KafkaBroker):
        self._broker = broker
        self._topic = "email_notifications"

    async def publish(self, message: TEmailMessage) -> None:
        await self._broker.publish(asdict(message), topic=self._topic)
