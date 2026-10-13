"""Existing databases receive schema changes; new ones are not migrated twice."""
import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine

from app.migrations import MIGRATIONS, apply_migrations

from ._app import Base, engine

EXPECTED_INDEXES = {
    "srs_cards": "ix_srs_cards_student_vocabulary",
    "student_progress": "ix_student_progress_student_lesson",
}


def _index_names(sync_conn, table):
    return {index["name"] for index in inspect(sync_conn).get_indexes(table)}


async def test_the_test_database_is_fully_migrated():
    async with engine.begin() as conn:
        assert await apply_migrations(conn) == []
        for table, index in EXPECTED_INDEXES.items():
            assert index in await conn.run_sync(_index_names, table)


async def test_a_database_from_before_the_indexes_is_upgraded_once(tmp_path):
    old = create_async_engine(f"sqlite+aiosqlite:///{(tmp_path / 'old.db').as_posix()}")
    try:
        async with old.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            for index in EXPECTED_INDEXES.values():           # as deployed before this change
                await conn.execute(text(f"DROP INDEX {index}"))
            await conn.execute(text(
                "INSERT INTO students (name, email, password_hash) VALUES ('a', 'a@example.com', 'x')"))

        async with old.begin() as conn:
            assert await apply_migrations(conn) == [migration_id for migration_id, _ in MIGRATIONS]
            for table, index in EXPECTED_INDEXES.items():
                assert index in await conn.run_sync(_index_names, table)
            assert (await conn.execute(text("SELECT COUNT(*) FROM students"))).scalar() == 1

        async with old.begin() as conn:
            assert await apply_migrations(conn) == []          # recorded: not applied again
    finally:
        await old.dispose()


async def test_tracking_upgrade_adds_only_its_tables_and_preserves_legacy_grades(tmp_path):
    old = create_async_engine(f"sqlite+aiosqlite:///{(tmp_path / 'before_tracking.db').as_posix()}")
    try:
        async with old.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            for table in reversed(Base.metadata.sorted_tables):
                if table.name.startswith("takip_"):
                    await conn.run_sync(lambda sync, table=table: table.drop(sync))
            await conn.execute(text("CREATE TABLE grade_entries (id INTEGER PRIMARY KEY, score INTEGER)"))
            await conn.execute(text("INSERT INTO grade_entries VALUES (7, 85)"))
            await conn.execute(text(
                "INSERT INTO students (id, name, email, password_hash, class_section) "
                "VALUES (23, 'Existing', 'existing@example.com', 'unchanged-hash', 'C')"))
            await apply_migrations(conn)
            assert (await conn.execute(text("SELECT id, score FROM grade_entries"))).all() == [(7, 85)]
            assert (await conn.execute(text(
                "SELECT id, password_hash, class_section FROM students"))).all() == [(23, "unchanged-hash", "C")]
            names = await conn.run_sync(lambda sync: inspect(sync).get_table_names())
            assert len([name for name in names if name.startswith("takip_")]) == 6
            for name in names:
                if name.startswith("takip_"):
                    assert (await conn.execute(text(f"SELECT COUNT(*) FROM {name}"))).scalar() == 0
            assert await apply_migrations(conn) == []
    finally:
        await old.dispose()


async def test_existing_accounts_gain_a_nullable_section_without_losing_activity(tmp_path):
    old = create_async_engine(f"sqlite+aiosqlite:///{(tmp_path / 'before_sections.db').as_posix()}")
    try:
        async with old.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            # A deployed account table that predates the section column.
            await conn.execute(text("DROP TABLE students"))
            await conn.execute(text(
                "CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT NOT NULL, "
                "email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, year INTEGER)"))
            await conn.execute(text(
                "INSERT INTO students VALUES (1, 'Existing', 'old@example.com', 'hash', 1)"))
            await conn.execute(text(
                "INSERT INTO units (id, unit_number, title_ar, title_tr) VALUES (1, 1, 'unit', 'unit')"))
            await conn.execute(text(
                "INSERT INTO lessons (id, unit_id, lesson_number, title_ar) VALUES (1, 1, 1, 'lesson')"))
            await conn.execute(text(
                "INSERT INTO student_progress (student_id, unit_id, lesson_id, score) VALUES (1, 1, 1, 42)"))
            await apply_migrations(conn)
            section = (await conn.execute(text("SELECT class_section FROM students WHERE id = 1"))).scalar()
            assert section is None
            assert (await conn.execute(text("SELECT score FROM student_progress"))).scalar() == 42
            for section in "ABCD":
                await conn.execute(text("UPDATE students SET class_section = :section"), {"section": section})
            with pytest.raises(IntegrityError):
                async with conn.begin_nested():
                    await conn.execute(text("UPDATE students SET class_section = 'E'"))

        async with old.begin() as conn:
            assert await apply_migrations(conn) == []
            section = (await conn.execute(text("SELECT class_section FROM students WHERE id = 1"))).scalar()
            assert section == "D"
    finally:
        await old.dispose()


async def test_section_migration_is_safe_when_column_already_exists(tmp_path):
    fresh = create_async_engine(f"sqlite+aiosqlite:///{(tmp_path / 'fresh.db').as_posix()}")
    try:
        async with fresh.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(text(
                "INSERT INTO students (name, email, password_hash, class_section) "
                "VALUES ('New', 'new@example.com', 'hash', 'B')"))
            await apply_migrations(conn)
            # A schema created from current models must tolerate an unrecorded migration.
            await conn.execute(text("DELETE FROM schema_migrations WHERE id = '0002_student_class_section'"))
            assert await apply_migrations(conn) == ["0002_student_class_section"]
            assert (await conn.execute(text("SELECT class_section FROM students"))).scalar() == "B"
    finally:
        await fresh.dispose()


async def test_section_upgrade_on_configured_database_preserves_activity(client, register, content):
    """Exercise ALTER TABLE on SQLite and on PostgreSQL when the suite uses it."""
    student = await register()
    await client.post("/api/me/progress/update", headers=student.headers, params={
        "unit_id": content.unit_a, "lesson_id": content.a_muf, "score": 10, "status": "completed"})
    async with engine.begin() as conn:
        await conn.execute(text("DROP INDEX ix_accounts_role_section"))
        await conn.execute(text("ALTER TABLE students DROP COLUMN class_section"))
        await conn.execute(text("DELETE FROM schema_migrations WHERE id = '0002_student_class_section'"))
        assert await apply_migrations(conn) == ["0002_student_class_section"]
        section = (await conn.execute(text("SELECT class_section FROM students WHERE id = :id"),
                                      {"id": student.id})).scalar()
        assert section is None
        assert (await conn.execute(text("SELECT score FROM student_progress"))).scalar() == 10
        await conn.execute(text("UPDATE students SET class_section = 'D' WHERE id = :id"), {"id": student.id})
        assert await apply_migrations(conn) == []
        await conn.execute(text("CREATE INDEX ix_accounts_role_section ON students (role, class_section)"))
    assert (await client.get("/api/auth/me", headers=student.headers)).json()["class_section"] == "D"


def test_migration_ids_are_unique_and_statements_are_repeatable():
    ids = [migration_id for migration_id, _ in MIGRATIONS]
    assert len(ids) == len(set(ids)) and ids == sorted(ids)
    for _, action in MIGRATIONS:
        if not callable(action):
            for statement in action:
                assert "IF NOT EXISTS" in statement.upper(), statement


@pytest.mark.parametrize("argv", [["--status"], []])
def test_migrate_tool_parses_its_arguments(argv, monkeypatch):
    from tools import migrate

    calls = []
    def fake_run(coroutine):
        calls.append(coroutine.__name__)
        coroutine.close()
        return 0

    monkeypatch.setattr(migrate.asyncio, "run", fake_run)
    assert migrate.main(argv) == 0
    assert calls == ["status" if argv else "migrate"]


async def test_upgrade_from_the_previous_release_keeps_accounts_and_grants_only_configured_roles(
        tmp_path, monkeypatch):
    """The deployed schema (no role/section/number columns) upgrades without touching records."""
    from types import SimpleNamespace

    from app import migrations
    from app.config import ADMIN_EMAIL

    monkeypatch.setattr(migrations, "get_settings",
                        lambda: SimpleNamespace(teacher_emails=frozenset({"teacher@karabuk.edu.tr"})))
    old = create_async_engine(f"sqlite+aiosqlite:///{(tmp_path / 'previous_release.db').as_posix()}")
    try:
        async with old.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(text("DROP TABLE students"))
            await conn.execute(text(
                "CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT NOT NULL, "
                "email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, university TEXT, "
                "department TEXT, year INTEGER, language_pref VARCHAR(5), created_at DATETIME, last_login DATETIME)"))
            for row in ((1, "Ali", "ali@example.com", "$2b$hash-ali"),
                        (2, "Teacher", "Teacher@Karabuk.edu.tr", "$2b$hash-teacher"),
                        (3, "Owner", ADMIN_EMAIL.upper(), "$2b$hash-owner"),
                        (4, "Dev", "dev-looking@example.com", "$2b$hash-dev")):
                await conn.execute(text(
                    "INSERT INTO students (id, name, email, password_hash, year) "
                    "VALUES (:i, :n, :e, :p, 1)"), dict(zip("inep", row, strict=True)))
            before = (await conn.execute(text(
                "SELECT id, name, email, password_hash FROM students ORDER BY id"))).all()

            await apply_migrations(conn)

            after = (await conn.execute(text(
                "SELECT id, name, email, password_hash FROM students ORDER BY id"))).all()
            assert after == before                                   # nothing rewritten or removed
            roles = dict((await conn.execute(text("SELECT id, role FROM students"))).all())
            assert roles == {1: "student", 2: "teacher", 3: "admin", 4: "student"}
            numbers = (await conn.execute(text(
                "SELECT COUNT(*) FROM students WHERE student_number IS NOT NULL OR class_section IS NOT NULL"))).scalar()
            assert numbers == 0                                      # no invented numbers or sections
            sections = (await conn.execute(text(
                "SELECT teacher_id, class_section FROM teacher_sections ORDER BY class_section"))).all()
            assert sections == [(2, "A"), (2, "B"), (2, "C"), (2, "D")]  # teacher keeps what they could see
            assert (await conn.execute(text("SELECT COUNT(*) FROM students WHERE is_active"))).scalar() == 4
    finally:
        await old.dispose()
