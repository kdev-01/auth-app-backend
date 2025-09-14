from functools import lru_cache

from src.core.config import get_settings

from .interface import IEmailService
from .smtp_service import SMTPEmailService


@lru_cache()
def provide_email_service() -> IEmailService:
    settings = get_settings()
    
    return SMTPEmailService(
        smtp_host=settings.SMTP_HOST,
        smtp_port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        use_tls=settings.SMTP_USE_TLS
    )
    