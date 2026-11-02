"""Password recovery mail. Credentials and the trusted link origin come from configuration."""
import smtplib
import ssl
from email.message import EmailMessage
from html import escape
from urllib.parse import urlencode, urlsplit

from app.config import get_settings


def mail_ready() -> bool:
    settings = get_settings()
    try:
        url = urlsplit(settings.password_reset_url)
        valid_url = (url.scheme == "https" and url.hostname and url.port in (None, 443)
                     and not url.username and not url.password and not url.query
                     and url.fragment == "/reset-password"
                     and not any(char.isspace() for char in settings.password_reset_url))
    except ValueError:
        return False
    return bool(settings.smtp_host and settings.smtp_from and valid_url
                and 1 <= settings.smtp_port <= 65535
                and bool(settings.smtp_username) == bool(settings.smtp_password)
                and not any(char in settings.smtp_from for char in "\r\n"))


def reset_message(address: str, token: str) -> EmailMessage:
    """Build both mail formats; links always use the server's configured origin."""
    settings = get_settings()
    link = f"{settings.password_reset_url}?{urlencode({'token': token})}"
    message = EmailMessage()
    message["Subject"] = "Arabiq Akademi — استعادة كلمة المرور / Şifre sıfırlama"
    message["From"] = settings.smtp_from
    message["To"] = address
    message.set_content(
        "لاستعادة كلمة مرور حسابك، افتح الرابط التالي خلال 20 دقيقة:\n\n"
        f"{link}\n\n"
        "الرابط يُستخدم مرة واحدة. إذا لم تطلب الاستعادة، تجاهل الرسالة.\n"
        "لا تشارك الرابط مع أحد. لن نطلب منك كلمة المرور عبر البريد.\n\n"
        "Şifrenizi sıfırlamak için yukarıdaki bağlantıyı 20 dakika içinde açın.\n"
        "Bağlantı tek kullanımlıktır. Bu isteği siz yapmadıysanız e-postayı yok sayın.\n"
        "Bağlantıyı kimseyle paylaşmayın.\n"
    )
    safe_link = escape(link, quote=True)
    message.add_alternative(f"""<!doctype html>
<html lang="ar" dir="rtl">
<body style="margin:0;background:#f6f5f1;color:#172d4d;font-family:Arial,sans-serif">
<div style="max-width:480px;margin:24px auto;padding:32px;background:#fff;border-radius:16px">
<p style="color:#96752d">Arabiq Akademi</p><h1 style="font-size:24px">استعادة كلمة المرور</h1>
<p style="line-height:1.9">اضغط على الزر لتعيين كلمة مرور جديدة لحسابك.</p>
<p style="margin:28px 0"><a href="{safe_link}"
style="background:#172d4d;color:#fff;padding:14px 24px;border-radius:8px;text-decoration:none">
تعيين كلمة مرور جديدة</a></p>
<p style="line-height:1.9">الرابط صالح لمدة 20 دقيقة ويُستخدم مرة واحدة.
إذا لم تطلب الاستعادة، تجاهل الرسالة. لا تشارك الرابط مع أحد.</p>
<hr style="border:0;border-top:1px solid #e6e6e6;margin:24px 0">
<div lang="tr" dir="ltr"><h2 style="font-size:20px">Şifre sıfırlama</h2>
<p style="line-height:1.8">Yeni şifrenizi belirlemek için yukarıdaki düğmeye tıklayın.
Bağlantı 20 dakika geçerlidir ve tek kullanımlıktır.
Bu isteği siz yapmadıysanız e-postayı yok sayın.</p></div>
<p style="font-size:12px;line-height:1.8">إذا لم يعمل الزر، انسخ الرابط وافتحه في المتصفح:</p>
<p dir="ltr" style="font-size:12px;word-break:break-all"><a href="{safe_link}">{safe_link}</a></p>
</div></body></html>""", subtype="html")
    return message


def send_reset_email(address: str, token: str) -> None:
    if not mail_ready():
        raise ValueError("Password recovery mail is not configured")
    settings = get_settings()
    message = reset_message(address, token)
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
