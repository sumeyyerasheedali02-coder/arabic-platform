"""Schema changes for databases that already exist.

`Base.metadata.create_all` only creates what is missing as a whole table; it
never alters an existing one. Anything added to an existing table (an index,
a column) therefore needs a migration here as well as in app/models.py.

Rules:
- append to MIGRATIONS, never edit or reorder an entry that has shipped;
- every statement must be valid on both SQLite and PostgreSQL;
- a migration must be safe to run on a database that already has the change
  (new databases get it from create_all first). Use IF NOT EXISTS where supported,
  or inspect the schema before adding columns (SQLite has no ADD COLUMN IF NOT EXISTS).

Applied migrations are recorded in the `schema_migrations` table. They run at
application start and with `python -m tools.migrate`.
"""
import logging
from collections.abc import Awaitable, Callable

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncConnection

from app.config import ADMIN_EMAIL, get_settings
from app.legacy_schema import align_legacy_sections

logger = logging.getLogger(__name__)

async def _add_student_class_section(conn: AsyncConnection) -> None:
    columns = await conn.run_sync(lambda sync: inspect(sync).get_columns("students"))
    if "class_section" not in {column["name"] for column in columns}:
        await conn.execute(text(
            "ALTER TABLE students ADD COLUMN class_section VARCHAR(1) "
            "CONSTRAINT ck_students_class_section CHECK (class_section IN ('A', 'B', 'C', 'D'))"
        ))


MigrationAction = tuple[str, ...] | Callable[[AsyncConnection], Awaitable[None]]


async def _add_staff_roles(conn: AsyncConnection) -> None:
    await align_legacy_sections(conn)
    columns = await conn.run_sync(lambda sync: inspect(sync).get_columns("students"))
    names = {column["name"] for column in columns}
    additions = {
        "role": "VARCHAR(10) NOT NULL DEFAULT 'student' CONSTRAINT ck_accounts_role "
                "CHECK (role IN ('student', 'teacher', 'admin'))",
        "is_active": "BOOLEAN NOT NULL DEFAULT true",
        "token_version": "INTEGER NOT NULL DEFAULT 0",
    }
    for name, definition in additions.items():
        if name not in names:
            await conn.execute(text(f"ALTER TABLE students ADD COLUMN {name} {definition}"))
    # Import existing staff once. Future access is determined only by database roles.
    for email in sorted(get_settings().teacher_emails | {ADMIN_EMAIL}):
        role = "admin" if email == ADMIN_EMAIL else "teacher"
        await conn.execute(text(
            "UPDATE students SET role = :role WHERE id = "
            "(SELECT MIN(id) FROM students WHERE LOWER(email) = :email) AND role = 'student'"
        ), {"role": role, "email": email})
        if role == "teacher":
            # Teachers could see every student before sections existed; keep that
            # until an administrator narrows it, instead of silently locking them out.
            tables = await conn.run_sync(lambda sync: inspect(sync).get_table_names())
            if "teacher_sections" in tables:
                for section in ("A", "B", "C", "D"):
                    await conn.execute(text(
                        "INSERT INTO teacher_sections (teacher_id, class_section) "
                        "SELECT id, CAST(:section AS VARCHAR(1)) FROM students "
                        "WHERE LOWER(email) = :email AND role = 'teacher' "
                        "AND NOT EXISTS (SELECT 1 FROM teacher_sections t "
                        "WHERE t.teacher_id = students.id "
                        "AND t.class_section = CAST(:section AS VARCHAR(1)))"
                    ), {"section": section, "email": email})
    await conn.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_accounts_role_section ON students (role, class_section)"))


async def _add_student_number(conn: AsyncConnection) -> None:
    columns = await conn.run_sync(lambda sync: inspect(sync).get_columns("students"))
    if "student_number" not in {column["name"] for column in columns}:
        await conn.execute(text("ALTER TABLE students ADD COLUMN student_number VARCHAR(32)"))
    # NULL remains valid for staff and existing students; never invent numbers.
    await conn.execute(text(
        "CREATE UNIQUE INDEX IF NOT EXISTS ux_students_student_number ON students (student_number)"))


async def _add_tracking_tables(conn: AsyncConnection) -> None:
    from app.tracking.models import (
        TrackingAudit,
        TrackingCycle,
        TrackingEntry,
        TrackingExam,
        TrackingTerm,
        TrackingWeek,
    )

    for model in (TrackingCycle, TrackingWeek, TrackingEntry, TrackingTerm, TrackingExam, TrackingAudit):
        await conn.run_sync(lambda sync, table=model.__table__: table.create(sync, checkfirst=True))

async def _add_activity_tables(conn: AsyncConnection) -> None:
    from app.models import ActivityClock, ActivitySession

    for model in (ActivityClock, ActivitySession):
        await conn.run_sync(lambda sync, table=model.__table__: table.create(sync, checkfirst=True))


async def _unique_srs_cards(conn: AsyncConnection) -> None:
    # Of each student's copies of one word keep the one with the most review
    # progress (latest review, then most repetitions), then the oldest.
    removed = (await conn.execute(text(
        "DELETE FROM srs_cards WHERE id IN (SELECT id FROM ("
        "SELECT id, ROW_NUMBER() OVER (PARTITION BY student_id, vocabulary_id ORDER BY "
        "CASE WHEN last_reviewed IS NULL THEN 1 ELSE 0 END, last_reviewed DESC, "
        "repetitions DESC, id) AS position FROM srs_cards "
        "WHERE student_id IS NOT NULL AND vocabulary_id IS NOT NULL) ranked "
        "WHERE position > 1)"))).rowcount
    logger.info("0008_unique_srs_cards: removed %s duplicate review card(s)", removed)
    await conn.execute(text(
        "CREATE UNIQUE INDEX IF NOT EXISTS ux_srs_cards_student_vocabulary "
        "ON srs_cards (student_id, vocabulary_id)"))
    # Same columns as the unique index; no longer needed.
    await conn.execute(text("DROP INDEX IF EXISTS ix_srs_cards_student_vocabulary"))


MIGRATIONS: tuple[tuple[str, MigrationAction], ...] = (
    # Lookups by student were full table scans. Measured on SQLite with 300
    # students: the due-cards query 9.1 ms -> 0.05 ms, a card lookup
    # 18.5 ms -> 0.04 ms, a student's progress 0.75 ms -> 0.12 ms.
    ("0001_student_lookup_indexes", (
        "CREATE INDEX IF NOT EXISTS ix_srs_cards_student_vocabulary "
        "ON srs_cards (student_id, vocabulary_id)",
        "CREATE INDEX IF NOT EXISTS ix_student_progress_student_lesson "
        "ON student_progress (student_id, lesson_id)",
    )),
    ("0002_student_class_section", _add_student_class_section),
    ("0003_staff_roles", _add_staff_roles),
    ("0004_student_number", _add_student_number),
    ("0005_legacy_section_compatibility", align_legacy_sections),
    ("0006_independent_grade_tracking", _add_tracking_tables),
    ("0007_student_active_time", _add_activity_tables),
    # Two simultaneous "add unit to review" requests created every card twice,
    # and every later review of such a word failed with a server error, so
    # neither copy progressed after that: keep the oldest of each group.
    ("0008_unique_srs_cards", _unique_srs_cards),
)

_CREATE_LOG = text(
    "CREATE TABLE IF NOT EXISTS schema_migrations ("
    "id VARCHAR(100) PRIMARY KEY, "
    "applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
)


async def applied_migrations(conn) -> set[str]:
    await conn.execute(_CREATE_LOG)
    return set((await conn.execute(text("SELECT id FROM schema_migrations"))).scalars().all())


async def apply_migrations(conn) -> list[str]:
    """Run the migrations that are not recorded yet; returns their ids."""
    done = await applied_migrations(conn)
    newly_applied = []
    for migration_id, action in MIGRATIONS:
        if migration_id in done:
            continue
        if callable(action):
            await action(conn)
        else:
            for statement in action:
                await conn.execute(text(statement))
        await conn.execute(text("INSERT INTO schema_migrations (id) VALUES (:id)"), {"id": migration_id})
        newly_applied.append(migration_id)
        logger.info("Applied database migration %s", migration_id)
    return newly_applied
