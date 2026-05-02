from .base import BaseDTO


class EmailNotificationDTO(BaseDTO):
    recipient: str
    subject: str
    content: str
