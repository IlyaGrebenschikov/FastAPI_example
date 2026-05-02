import logging
from dataclasses import dataclass

from fastapi_example.infrastructure import AppSettings, CORSSettings, SMTPSettings

log = logging.getLogger(__name__)


@dataclass
class V1APISettings:
    app: AppSettings
    cors: CORSSettings


@dataclass
class EmailNotificationSettings:
    sender: str


@dataclass
class ApplicationSettings:
    v1_api: V1APISettings
    email_notifications: EmailNotificationSettings


def load_application_settings(
    app_settings: AppSettings, cors_settings: CORSSettings, smtp_settings: SMTPSettings
) -> ApplicationSettings:
    log.debug("Loading application settings.")
    v1_api = V1APISettings(app=app_settings, cors=cors_settings)
    email_notifications = EmailNotificationSettings(smtp_settings.sender)
    return ApplicationSettings(v1_api, email_notifications)
