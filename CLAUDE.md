# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Arabic language learning platform ("العربية بين يديك") for Turkish theology students at Karabük University. Built with a FastAPI backend and a React + Vite frontend. The AI tutor feature uses the Google Gemini API.

## Running the Servers

**Backend** (from `files_extracted/`):
```bash
uvicorn main:app --reload --port 8000
```

**Frontend** (from `frontend/`):
```bash
npm run dev        # dev server on http://localhost:5173
npm run build      # production build
npm run lint       # ESLint
```

**Seed the database** (run once after first backend startup):
```bash
cd files_extracted
python seed_database.py
```

The backend auto-creates `arabic_platform.db` (SQLite) on first startup via `init_db()`. Re-running `seed_database.py` will duplicate data — only run it on a fresh database.

## Environment Variables (`files_extracted/.env`)

```
SECRET_KEY=...                  # JWT signing key
GOOGLE_API_KEY=...              # Gemini API — required for /api/chat
DATABASE_URL=sqlite+aiosqlite:///./arabic_platform.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

## Architecture

### Backend (`files_extracted/`)

- **`main.py`** — All FastAPI routes. No separate router files; everything is inline. Protected endpoints use `Depends(get_current_student)` from `auth.py`.
- **`database.py`** — All SQLAlchemy async models and the `get_db` session dependency. `init_db()` is called on app startup.
- **`auth.py`** — JWT creation/validation using `python-jose`. Password hashing uses `bcrypt` directly (not passlib — passlib 1.7.4 is incompatible with bcrypt 5.x). The `sub` claim in JWTs is stored as a **string** and converted to `int` on decode.
- **`schemas.py`** — Pydantic v2 models for request/response. Uses `model_config = {"from_attributes": True}` for ORM serialisation.
- **`srs.py`** — Pure SM-2 spaced repetition algorithm. No database access; takes and returns dataclasses.
- **`unit_1.py`** — Flat Python dict with all content for Unit 1 (vocabulary, dialogues, exercises). New units follow this same structure under a `data/` directory.

### Key backend relationships

```
Unit → Lesson → Dialogue → DialogueLine
Unit → Lesson → Exercise
Unit → Vocabulary ← SRSCard ← Student
Student → StudentProgress → (Unit, Lesson)
Student → ExerciseAnswer → Exercise
Student → AISession
```

All foreign keys use `ondelete="CASCADE"` except `Vocabulary.lesson_id` (`SET NULL`).

### Authentication flow

Login/register both return a `Token` with `access_token`. Protected routes extract the student ID via `OAuth2PasswordBearer` → `get_current_student()`. The login endpoint uses OAuth2 form encoding (`application/x-www-form-urlencoded`), not JSON.

### AI Chat (`POST /api/chat`)

Uses `google.generativeai` (configured at module level in `main.py`). Sends the full message history each request — the backend splits it into `history[:-1]` and the last message for Gemini's `start_chat` / `send_message_async`. The system prompt injects unit vocabulary context when `unit_id` is provided.

### Frontend (`frontend/src/`)

- **`api/client.js`** — Axios instance with `baseURL: '/api'`. Request interceptor attaches Bearer token from localStorage. Response interceptor redirects to `/login` on 401, **except** for `/auth/` endpoints (to allow login error messages to surface).
- **`context/AuthContext.jsx`** — JWT token and student info in React state + localStorage. `loading: true` until the initial localStorage check completes — `ProtectedRoute` waits for this before deciding to redirect.
- **`App.jsx`** — All routes defined here. Protected pages are wrapped with `<ProtectedRoute><Layout>`.
- **`pages/`** — Five pages: `LoginRegister`, `Dashboard`, `Lessons`, `Chat`, `SRSFlashcards`. Pages fetch their own data on mount; no global data store.

The Vite dev server proxies `/api/*` to `http://localhost:8000` — no CORS configuration needed in development.

### Adding a new unit

1. Create `files_extracted/data/unit_N.py` following the structure of `unit_1.py`.
2. Add a seed block in `seed_database.py` importing and inserting `UNIT_N`.
3. Run `seed_database.py` against a fresh database (or write a migration).

## Known Compatibility Issues

- `passlib` must **not** be used with `bcrypt` — use `bcrypt` directly. `passlib 1.7.4` + `bcrypt >=4.0` causes a `ValueError` on every hash/verify call.
- `python-jose` v3.5+ requires JWT `sub` to be a string. Always use `str(student.id)` when creating tokens and `int(sub)` when decoding.
- `pydantic-core` has no pre-built wheel for Python 3.14. Install dependencies without pinned versions so pip resolves compatible wheels.
