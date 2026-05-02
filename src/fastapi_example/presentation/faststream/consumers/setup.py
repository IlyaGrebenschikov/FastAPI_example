from faststream.kafka import KafkaBroker, KafkaRouter


def setup_routers(broker: KafkaBroker, *routers: KafkaRouter) -> None:
    for router in routers:
        broker.include_router(router)
