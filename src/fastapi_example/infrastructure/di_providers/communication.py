from typing import Any, AsyncGenerator

import aiosmtplib
from dishka import Provider, Scope, provide

from fastapi_example.infrastructure import SMTPSettings
from fastapi_example.infrastructure.communication.email import create_smtp_client


class EmailCommunicationProvider(Provider):
    def __init__(self, settings: SMTPSettings, scope=None, component=None):
        super().__init__(scope, component)
        self._settings = settings

    @provide(scope=Scope.APP)
    async def smtp_client(self) -> AsyncGenerator[aiosmtplib.SMTP, Any]:
        client = create_smtp_client(self._settings)
        async with client:
            if self._settings.username and self._settings.password:
                await client.login(self._settings.username, self._settings.password)
            yield client
            