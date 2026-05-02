from fastapi_example.application.interfaces.communication import TEmailMessage


class IEmailNotificationsProducer:
    async def publish(self, message: TEmailMessage) -> None: ...
