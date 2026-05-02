from faststream.kafka import KafkaRouter
from dishka.integrations.faststream import FromDishka

from fastapi_example.presentation.faststream.dto import EmailNotificationDTO
from fastapi_example.application.interfaces.services import IEmailNotificationsService, TEmailMessage


email_notifications_router = KafkaRouter()


@email_notifications_router.subscriber("email-notifications")
async def email_notifications(
        message: FromDishka[EmailNotificationDTO],
        service: FromDishka[IEmailNotificationsService]
) -> None:
    data = TEmailMessage(subject=message.subject, recipient=message.recipient, content=message.content)
    await service.send(data)
