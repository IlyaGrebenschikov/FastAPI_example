from faststream.kafka import KafkaBroker

from fastapi_example.core.settings import MessageBrokerSettings


def create_broker(settings: MessageBrokerSettings) -> KafkaBroker:
    return KafkaBroker(settings.url)
