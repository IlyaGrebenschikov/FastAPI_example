from dishka import Provider, Scope, provide

from fastapi_example.application.interfaces.services import (
    IEmailNotificationsService,
)
from fastapi_example.application.interfaces.message_broker.producers import IEmailNotificationsProducer
from fastapi_example.application.interfaces.communication import IEmailSender
from fastapi_example.application.services import EmailNotificationsService
from fastapi_example.application.settings import EmailNotificationSettings


class EmailNotificationsServiceProvider(Provider):
    def __init__(self, settings: EmailNotificationSettings, scope=None, component=None):
        super().__init__(scope, component)
        self._settings = settings

    @provide(scope=Scope.REQUEST)
    def email_notifications(self, producer: IEmailNotificationsProducer, sender: IEmailSender) -> IEmailNotificationsService:
        return EmailNotificationsService(producer, sender, self._settings)
