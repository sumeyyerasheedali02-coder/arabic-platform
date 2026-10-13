import pytest

from ._app import load_secret_key


@pytest.mark.parametrize("value", [None, "", "   ", "change-this-secret", "your-secret-key-here"])
def test_missing_or_placeholder_secret_is_replaced_by_a_random_key(monkeypatch, value):
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    if value is None:
        monkeypatch.delenv("SECRET_KEY", raising=False)
    else:
        monkeypatch.setenv("SECRET_KEY", value)
    first, second = load_secret_key(), load_secret_key()
    assert first != second and len(first) >= 48
    assert first not in ("change-this-secret", "your-secret-key-here")


def test_production_refuses_to_start_without_a_real_secret(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("SECRET_KEY", "change-this-secret")
    with pytest.raises(RuntimeError):
        load_secret_key()


def test_configured_secret_is_used_as_is(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("SECRET_KEY", "a-real-configured-secret-value")
    assert load_secret_key() == "a-real-configured-secret-value"


def test_settings_parse_lists_flags_and_database_urls(monkeypatch):
    from app.config import Settings, normalize_database_url

    monkeypatch.setenv("TEACHER_EMAILS", " Hoca@Example.com , ,second@example.com")
    monkeypatch.setenv("CORS_ORIGINS", "https://a.example, http://localhost:5173")
    monkeypatch.setenv("SEED_ON_EMPTY_DB", "no")
    settings = Settings.from_env()
    assert settings.teacher_emails == {"hoca@example.com", "second@example.com"}
    assert settings.is_teacher_email("HOCA@example.com") and not settings.is_teacher_email(None)
    assert settings.cors_origins == ("https://a.example", "http://localhost:5173")
    assert settings.seed_on_empty_db is False

    assert normalize_database_url("postgres://u:p@h/db") == "postgresql+asyncpg://u:p@h/db"
    assert normalize_database_url("postgresql://u:p@h/db") == "postgresql+asyncpg://u:p@h/db"
    assert normalize_database_url("sqlite+aiosqlite:///./x.db") == "sqlite+aiosqlite:///./x.db"
