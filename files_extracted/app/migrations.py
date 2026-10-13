"""Schema changes for databases that already exist.

`Base.metadata.create_all` only creates what is missing as a whole table; it
never alters an existing one. Anything added to an existing table (an index,
a column) therefore needs a migration here as well as in app/models.py.

Rules:
- append to MIGRATIONS, never edit or reorder an entry that has shipped;
- every statement must be valid on both SQLite and PostgreSQL;
- a migration must be safe to run on a database that already has the change
  (new databases get it from create_all first), hence IF NOT EXISTS.

Applied migrations are recorded in the `schema_migrations` table. They run at
application start and with `python -m tools.migrate`.
"""
import logging

from sqlalchemy import text

logger = logging.getLogger(__name__)

MIGRATIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
    # Lookups by student were full table scans. Measured on SQLite with 300
    # students: the due-cards query 9.1 ms -> 0.05 ms, a card lookup
    # 18.5 ms -> 0.04 ms, a student's progress 0.75 ms -> 0.12 ms.
    ("0001_student_lookup_indexes", (
        "CREATE INDEX IF NOT EXISTS ix_srs_cards_student_vocabulary "
        "ON srs_cards (student_id, vocabulary_id)",
        "CREATE INDEX IF NOT EXISTS ix_student_progress_student_lesson "
        "ON student_progress (student_id, lesson_id)",
    )),
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
    for migration_id, statements in MIGRATIONS:
        if migration_id in done:
            continue
        for statement in statements:
            await conn.execute(text(statement))
        await conn.execute(text("INSERT INTO schema_migrations (id) VALUES (:id)"), {"id": migration_id})
        newly_applied.append(migration_id)
        logger.info("Applied database migration %s", migration_id)
    return newly_applied
