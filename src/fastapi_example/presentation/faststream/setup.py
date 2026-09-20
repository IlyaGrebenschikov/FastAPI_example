from dishka import AsyncContainer
from dishka.integrations.faststream import setup_dishka
from faststream import FastStream
from faststream.kafka import KafkaBroker

from .consumers import email_notifications_router, setup_routers


async def init_faststream(di_container: AsyncContainer) -> FastStream:
    broker = await di_container.get(KafkaBroker)
    setup_routers(broker, email_notifications_router)
    app = FastStream(broker)
    setup_dishka(di_container, app, auto_inject=True)
    return app
