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
