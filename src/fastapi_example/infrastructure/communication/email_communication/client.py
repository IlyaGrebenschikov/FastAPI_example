import aiosmtplib

from fastapi_example.infrastructure.settings import SMTPSettings


def create_smtp_client(settings: SMTPSettings) -> aiosmtplib.SMTP:
    return aiosmtplib.SMTP(
        hostname=settings.host,
        port=settings.port,
        use_tls=settings.use_tls
    )
