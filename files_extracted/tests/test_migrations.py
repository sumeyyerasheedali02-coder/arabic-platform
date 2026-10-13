"""Existing databases receive schema changes; new ones are not migrated twice."""
import pytest
from sqlalchemy import inspect, text
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


def test_migration_ids_are_unique_and_statements_are_repeatable():
    ids = [migration_id for migration_id, _ in MIGRATIONS]
    assert len(ids) == len(set(ids)) and ids == sorted(ids)
    for _, statements in MIGRATIONS:
        for statement in statements:
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
