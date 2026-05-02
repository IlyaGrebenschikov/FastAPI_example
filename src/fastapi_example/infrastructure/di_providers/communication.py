from typing import Any, AsyncGenerator

import aiosmtplib
from dishka import Provider, Scope, provide

from fastapi_example.infrastructure import SMTPSettings
from fastapi_example.infrastructure.communication.email import EmailSender, create_smtp_client


class CommunicationProvider(Provider):
    def __init__(self, smtp_settings: SMTPSettings, scope=None, component=None):
        super().__init__(scope, component)
        self._smtp_settings = smtp_settings

    @provide(scope=Scope.APP)
    async def smtp_client(self) -> AsyncGenerator[aiosmtplib.SMTP, Any]:
        client = create_smtp_client(self._smtp_settings)
        async with client:
            if self._smtp_settings.username and self._smtp_settings.password:
                await client.login(self._smtp_settings.username, self._smtp_settings.password)
            yield client

    @provide(scope=Scope.APP)
    def email_sender(self, client: aiosmtplib.SMTP) -> EmailSender:
        return EmailSender(client, self._smtp_settings.sender)
