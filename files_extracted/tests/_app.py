"""Single import point for application objects used by the tests.

The environment is pointed at a throw-away SQLite file *before* any
application module is imported, so the suite can never touch a real database.
Only this module needs to change when application modules move.
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

os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{TEST_DB_PATH.as_posix()}"
os.environ["SECRET_KEY"] = TEST_SECRET
os.environ["TEACHER_EMAILS"] = TEACHER_EMAIL
os.environ["GOOGLE_API_KEY"] = "test-key-not-real"
os.environ["ALGORITHM"] = "HS256"

import database as models  # noqa: E402
import main as main_module  # noqa: E402
from auth import hash_password, load_secret_key  # noqa: E402
from database import AsyncSessionLocal, Base, engine, init_db  # noqa: E402
from main import app  # noqa: E402

__all__ = [
    "AsyncSessionLocal", "Base", "TEACHER_EMAIL", "TEST_DB_PATH", "TEST_SECRET",
    "app", "engine", "hash_password", "init_db", "load_secret_key", "main_module", "models",
]
