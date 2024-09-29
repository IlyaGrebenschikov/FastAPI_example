from typing import Callable

from backend.src.database.gateway import DBGateway
from backend.src.services.gateway import ServiceGateway

ServiceGatewayFactory = Callable[[], ServiceGateway]


def create_service_gateway_factory(
    database: Callable[[], DBGateway],
) -> ServiceGatewayFactory:
    def _create_instance() -> ServiceGateway:
        return ServiceGateway(database())

    return _create_instance
