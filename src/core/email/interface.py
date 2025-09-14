from typing import Protocol

from .schemas import EmailMessage


class IEmailService(Protocol):
    def send_email(self, message: EmailMessage) -> None: ...
    