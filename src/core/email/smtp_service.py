import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .schemas import EmailMessage


class SMTPEmailService:
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        use_tls: bool = True
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def send_email(self, message: EmailMessage) -> None:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = message.subject
        msg["From"] = message.from_email
        msg["To"] = ", ".join(message.to)

        content_type = "html" if message.html else "plain"
        part = MIMEText(message.body, content_type)
        msg.attach(part)

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            if self.use_tls:
                server.starttls()
            server.login(self.username, self.password)
            server.sendmail(message.from_email, message.to, msg.as_string())
