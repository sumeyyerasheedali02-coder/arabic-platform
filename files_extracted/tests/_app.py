"""Single import point for application objects used by the tests.

The environment is pointed at a throw-away SQLite file *before* any
application module is imported, so the suite can never touch a real database.
Only this module needs to change when application modules move.

To run the suite on another engine (PostgreSQL), set TEST_DATABASE_URL to a
database that exists only for this purpose. Its name must contain
"arabiq_test": the tests empty every table in it.
"""
import os
import sys
import tempfile
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

_TMP_DIR = Path(tempfile.mkdtemp(prefix="arabiq-test-"))
TEST_DB_PATH = _TMP_DIR / "test.db"
TEACHER_EMAIL = "teacher@example.com"
TEST_SECRET = "test-only-signing-key-0123456789abcdef"

TEST_DATABASE_MARKER = "arabiq_test"
_override = os.environ.get("TEST_DATABASE_URL", "").strip()
if _override:
    if TEST_DATABASE_MARKER not in _override.rsplit("/", 1)[-1]:
        raise RuntimeError(
            f"TEST_DATABASE_URL must name a database containing {TEST_DATABASE_MARKER!r}; "
            "the tests delete every row in it")
    os.environ["DATABASE_URL"] = _override
else:
    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{TEST_DB_PATH.as_posix()}"
os.environ["SECRET_KEY"] = TEST_SECRET
os.environ["TEACHER_EMAILS"] = TEACHER_EMAIL
os.environ["GOOGLE_API_KEY"] = "test-key-not-real"
os.environ["ALGORITHM"] = "HS256"

import main as main_module  # noqa: E402
from app import models  # noqa: E402
from app.config import load_secret_key  # noqa: E402
from app.database import AsyncSessionLocal, Base, engine, init_db  # noqa: E402
from app.security import hash_password  # noqa: E402
from app.services import ai as ai_service  # noqa: E402
from main import app  # noqa: E402

__all__ = [
    "AsyncSessionLocal", "Base", "TEACHER_EMAIL", "TEST_DB_PATH", "TEST_SECRET",
    "ai_service", "app", "engine", "hash_password", "init_db", "load_secret_key",
    "main_module", "models",
]
