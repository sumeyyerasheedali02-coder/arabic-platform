"""All runtime configuration, read once from the environment (and `.env`)."""
import logging
import os
import secrets
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///./arabic_platform.db"
DEFAULT_CORS_ORIGINS = "https://arabic-platform-flame.vercel.app,http://localhost:5173"
DEFAULT_GEMINI_MODEL = "gemini-3.5-flash-lite"

# Values that are public knowledge (old code default, .env.example placeholder).
# Anyone can forge a login token for any account if one of them signs the tokens.
INSECURE_SECRET_KEYS = {"", "change-this-secret", "your-secret-key-here"}


def _flag(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def _csv(raw: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in raw.split(",") if item.strip())


def normalize_database_url(url: str) -> str:
    """Railway hands out postgres:// or postgresql://; asyncpg needs its driver prefix."""
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    if url.startswith("postgresql://") and "+asyncpg" not in url:
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


def load_secret_key() -> str:
    """Return the JWT signing key, never a publicly known one.

    Without a real SECRET_KEY the process signs with a random key that lives
    only in memory: the API stays usable and safe, but every restart logs
    everyone out. Set ENVIRONMENT=production to refuse to start instead.
    """
    key = os.getenv("SECRET_KEY", "").strip()
    if key not in INSECURE_SECRET_KEYS:
        return key
    if os.getenv("ENVIRONMENT", "").strip().lower() == "production":
        raise RuntimeError(
            "SECRET_KEY is missing or is a placeholder. Generate one with "
            "`python -c \"import secrets; print(secrets.token_urlsafe(48))\"` "
            "and set it in the environment.")
    logger.warning(
        "SECRET_KEY is missing or is a placeholder: using a temporary random key. "
        "All logins become invalid when the server restarts. Set SECRET_KEY to fix this.")
    return secrets.token_urlsafe(48)


@dataclass(frozen=True)
class Settings:
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    teacher_emails: frozenset[str]
    cors_origins: tuple[str, ...]
    google_api_key: str
    gemini_model: str
    seed_on_empty_db: bool

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            database_url=normalize_database_url(os.getenv("DATABASE_URL") or DEFAULT_DATABASE_URL),
            secret_key=load_secret_key(),
            algorithm=os.getenv("ALGORITHM") or "HS256",
            access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 10080),
            teacher_emails=frozenset(e.lower() for e in _csv(os.getenv("TEACHER_EMAILS", ""))),
            cors_origins=_csv(os.getenv("CORS_ORIGINS") or DEFAULT_CORS_ORIGINS),
            google_api_key=os.getenv("GOOGLE_API_KEY", "").strip(),
            gemini_model=os.getenv("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL,
            seed_on_empty_db=_flag("SEED_ON_EMPTY_DB", True),
        )

    def is_teacher_email(self, email: str | None) -> bool:
        return (email or "").strip().lower() in self.teacher_emails


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()
