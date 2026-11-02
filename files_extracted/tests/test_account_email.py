from dataclasses import replace
from unittest.mock import MagicMock
from urllib.parse import parse_qs, urlsplit

import pytest

from app.config import get_settings
from app.services import account_email

from . import _app  # noqa: F401 - temporary database before application imports


@pytest.fixture
def mail_settings(monkeypatch):
    settings = replace(get_settings(), smtp_host="smtp.example.test", smtp_port=587,
                       smtp_username="sender", smtp_password="test-only-password",
                       smtp_from="Arabiq <sender@example.test>",
                       password_reset_url="https://arabic-kbu.vercel.app/#/reset-password")
    monkeypatch.setattr(account_email, "get_settings", lambda: settings)
    return settings


@pytest.mark.parametrize("url", [
    "http://example.test/#/reset-password", "https://user:pass@example.test/#/reset-password",
    "https://example.test/#/login", "https://example.test/?redirect=evil#/reset-password",
    "https://example.test:bad/#/reset-password", "https://example.test/#/reset-password\n",
])
def test_mail_refuses_untrusted_link_configuration(mail_settings, monkeypatch, url):
    monkeypatch.setattr(account_email, "get_settings", lambda: replace(mail_settings, password_reset_url=url))
    assert not account_email.mail_ready()


def test_mail_requires_complete_credentials(mail_settings, monkeypatch):
    assert account_email.mail_ready()
    monkeypatch.setattr(account_email, "get_settings", lambda: replace(mail_settings, smtp_password=""))
    assert not account_email.mail_ready()
    monkeypatch.setattr(account_email, "get_settings", lambda: replace(mail_settings, smtp_from=""))
    assert not account_email.mail_ready()


def test_bilingual_message_contains_one_trusted_link_in_both_formats(mail_settings):
    message = account_email.reset_message("student@example.test", "signed+token&value")
    assert message["To"] == "student@example.test"
    plain = message.get_body(preferencelist=("plain",)).get_content()
    html = message.get_body(preferencelist=("html",)).get_content()
    link = next(line for line in plain.splitlines() if line.startswith("https://"))
    assert urlsplit(link).hostname == "arabic-kbu.vercel.app"
    assert parse_qs(urlsplit(link).fragment.split("?", 1)[1])["token"] == ["signed+token&value"]
    assert link in html
    assert 'lang="ar" dir="rtl"' in html and 'lang="tr" dir="ltr"' in html
    assert "20" in plain and "20" in html
    assert "Şifrenizi" in plain


@pytest.mark.parametrize("port", [465, 587])
def test_smtp_encrypts_before_authentication(mail_settings, monkeypatch, port):
    monkeypatch.setattr(account_email, "get_settings", lambda: replace(mail_settings, smtp_port=port))
    factory = MagicMock()
    server = factory.return_value.__enter__.return_value
    monkeypatch.setattr(account_email.smtplib, "SMTP_SSL" if port == 465 else "SMTP", factory)
    other = MagicMock(side_effect=AssertionError("unexpected transport"))
    monkeypatch.setattr(account_email.smtplib, "SMTP" if port == 465 else "SMTP_SSL", other)
    account_email.send_reset_email("student@example.test", "signed-token")
    server.login.assert_called_once_with("sender", "test-only-password")
    server.send_message.assert_called_once()
    if port == 587:
        names = [call[0] for call in server.method_calls]
        assert names == ["ehlo", "starttls", "ehlo", "login", "send_message"]
        assert server.starttls.call_args.kwargs["context"].check_hostname
    else:
        assert factory.call_args.kwargs["context"].check_hostname
        server.starttls.assert_not_called()


def test_tls_failure_does_not_send_credentials_or_mail(mail_settings, monkeypatch):
    factory = MagicMock()
    server = factory.return_value.__enter__.return_value
    server.starttls.side_effect = OSError("test TLS failure")
    monkeypatch.setattr(account_email.smtplib, "SMTP", factory)
    with pytest.raises(OSError):
        account_email.send_reset_email("student@example.test", "signed-token")
    server.login.assert_not_called()
    server.send_message.assert_not_called()
