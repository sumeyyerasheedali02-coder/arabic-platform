"""Password recovery mail. Credentials and the trusted link origin come from configuration."""
import smtplib
import ssl
from email.message import EmailMessage
from urllib.parse import urlsplit

from app.config import get_settings


def mail_ready() -> bool:
    settings = get_settings()
    url = urlsplit(settings.password_reset_url)
    return bool(settings.smtp_host and settings.smtp_from
                and url.scheme == "https" and url.netloc
                and not url.username and not url.password and not url.query
                and url.fragment == "/reset-password")


def send_reset_email(address: str, token: str) -> None:
    settings = get_settings()
    message = EmailMessage()
    message["Subject"] = "Arabiq Akademi — استعادة كلمة المرور"
    message["From"] = settings.smtp_from
    message["To"] = address
    message.set_content(
        "لاستعادة كلمة مرور حسابك، افتح الرابط التالي خلال 20 دقيقة:\n\n"
        f"{settings.password_reset_url}?token={token}\n\n"
        "الرابط يُستخدم مرة واحدة. إذا لم تطلب الاستعادة، تجاهل الرسالة."
    )
    context = ssl.create_default_context()
    if settings.smtp_port == 465:
        connection = smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port,
                                     timeout=15, context=context)
    else:
        connection = smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15)
    with connection as server:
        if settings.smtp_port != 465:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
        if settings.smtp_username:
            server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(message)
