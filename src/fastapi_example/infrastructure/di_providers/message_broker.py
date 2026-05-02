from dishka import Provider, Scope, provide
from faststream.kafka import KafkaBroker

from fastapi_example.application.interfaces.message_broker.producers import (
    IEmailNotificationsProducer,
)
from fastapi_example.infrastructure import MessageBrokerSettings
from fastapi_example.infrastructure.message_broker import create_broker
from fastapi_example.infrastructure.message_broker.producers import (
    EmailNotificationsProducer,
)


class MessageBrokerProvider(Provider):
    def __init__(
        self, broker_settings: MessageBrokerSettings, scope=None, component=None
    ):
        super().__init__(scope, component)
        self._broker_settings = broker_settings

    @provide(scope=Scope.APP)
    def client(self) -> KafkaBroker:
        return create_broker(self._broker_settings)


class MessageBrokerProducersProvider(Provider):
    @provide(scope=Scope.APP)
    def email_notifications_producer(
        self, broker: KafkaBroker
    ) -> IEmailNotificationsProducer:
        return EmailNotificationsProducer(broker)
