# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

Arabiq Akademi ("العربية بين يديك"): an Arabic learning platform for Turkish theology students at Karabük University. FastAPI backend in `files_extracted/`, React + Vite frontend in `frontend/`. The AI tutor uses Google Gemini.

Read `PROJECT_MAP.md` (Arabic) for the full map: routes, data model, content, and "where do I change X". This file only lists what you must know before editing.

## Commands

Backend (from `files_extracted/`, Python 3.12, virtualenv in `.venv`):

```bash
uvicorn main:app --reload --port 8000
pytest -q                 # throw-away SQLite database
ruff check .
python -m tools.seed --help            # content loading
python -m tools.migrate --status       # schema migrations
python -m tools.content_report         # read-only summary of a database
python -m tools.update_dialogues       # dialogues of a live database (dry run; --apply)
python -m tools.teacher_accounts list  # teacher provisioning
```

Frontend (from `frontend/`, Node 22):

```bash
npm run dev      # http://localhost:5173, /api proxied to localhost:8000
npm run lint
npm test         # node --test, pure logic only
npm run build
```

## Hard rules

- **Never run a tool against a database you have not identified.** Every tool uses `DATABASE_URL` at the moment it runs. `tools.seed --replace` deletes every student's answers, progress and review cards.
- **No secrets in tracked files.** Configuration comes from the environment (`files_extracted/.env.example`, `app/config.py`). Keys were leaked through helper scripts once; see `SECURITY.md`.
- **No one-off patch scripts.** Edit the source. ~130 `fix_*.py`-style scripts were removed; do not reintroduce the pattern.
- **Content is edited in `files_extracted/content/`**, never in the database by hand.
- **Preserve the visual design.** Styling is mostly inline `style` objects; when splitting or moving a component, copy the values exactly. Arabic is RTL; Turkish/English text gets `dir="ltr"`.
- Do not deploy or push without being asked.

## Backend architecture (`files_extracted/`)

- `main.py` only assembles the app (settings, lifespan, CORS, routers).
- `app/config.py`: every environment variable, read once into a frozen `Settings`.
- `app/database.py`: engine, session factory, `get_db`, `init_db` (create tables + apply migrations).
- `app/models.py`: ORM models. `app/schemas.py`: Pydantic models.
- `app/security.py`: bcrypt, JWT, `get_current_account` / `get_current_student` / `get_current_teacher`.
- `app/routers/`: one module per feature (`auth`, `content`, `exercises`, `progress`, `srs`, `chat`, `teacher`). Routers handle HTTP only.
- `app/services/`: reusable logic (`answers`, `exercise_categories`, `srs` (SM-2), `ai`, `reporting`).
- `app/migrations.py`: ordered, recorded changes for existing databases.
- `content/`: pure data (books, exercise sets, `labels.py`). No database access.
- `tools/`: command-line tools (`seed`, `migrate`, `teacher_accounts`, `content_report`).
- `tests/`: API-level tests. `tests/_app.py` is the only place that imports application modules for the suite and points it at a temporary database first.

Relationships: `Unit → Lesson → Dialogue → DialogueLine`, `Unit → Lesson → Exercise`, `Unit → Vocabulary ← SRSCard ← Student`, `Student → StudentProgress → (Unit, Lesson)`, `Student → ExerciseAnswer → Exercise`.

### Things that bite

- **Schema changes need a migration.** `create_all` never alters an existing table. Change `app/models.py` *and* append to `MIGRATIONS` in `app/migrations.py` (statements must work on SQLite and PostgreSQL and be repeatable).
- **SQLite does not enforce foreign keys; PostgreSQL does.** Anything that deletes rows must be tested on PostgreSQL (`TEST_DATABASE_URL`, database name containing `arabiq_test`).
- **Column defaults exist only after flush.** A freshly constructed ORM object has `None` in defaulted columns (this caused a 500 in SRS review).
- **bcrypt directly, not passlib** (passlib 1.7.4 breaks with bcrypt ≥ 4). Passwords over 72 bytes are rejected.
- **JWT `sub` is a string** (`str(student.id)`); python-jose requires it.
- **Async sessions cannot lazy-load.** Use `selectinload` (see dialogues).
- **Arabic text comparison:** two strings can look identical and differ in the order of combining marks. Never compare vocalised Arabic exactly; normalise with `app/services/answers.normalize_answer`. Category texts are constants in `content/labels.py`.
- **Teacher rights** = account e-mail listed in `TEACHER_EMAILS`. Those addresses cannot self-register; e-mail lookups are case-insensitive.
- The login endpoint takes OAuth2 form encoding (`username`, `password`), not JSON.
- Tests mock the AI provider by replacing `app.services.ai.get_client`; never call the real provider from tests.

## Frontend architecture (`frontend/src/`)

- `api/config.js` decides the backend address (`VITE_API_URL`; unset in development → relative `/api` through the Vite proxy). `api/client.js` is the only axios instance; it attaches the token and reports a rejected session.
- `api/useApiData.js`: `useApiData(key, load)` → `{ data, loading, error, reload }`. Use it for every data fetch.
- `auth/`: `AuthProvider` (inside the router), `useAuth`, `session.js` (stored login; pure, tested).
- `layout/AppLayout.jsx` mounts `UnitsProvider` and `ProgressProvider` once; pages read `useUnits()` / `useProgress()`. The selected unit lives only there.
- `features/<name>/`: one folder per page. Pure logic sits in `.js` files next to the components and is tested in `frontend/tests/`.
- `components/`: `Spinner`, `ErrorState`, `BrandMark`.
- `HashRouter`; pages are lazy-loaded in `App.jsx`. Guests can open every page except `/teacher`.

## Adding content

See `files_extracted/content/README.md`. In short: edit the data module, try it on a scratch database with `tools.seed`, check with `tools.content_report`, then decide how to apply it to a database that students use (dialogues: `tools.update_dialogues`).
