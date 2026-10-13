"""Bring the database named by DATABASE_URL up to the current schema.

    python -m tools.migrate            # create missing tables, apply pending migrations
    python -m tools.migrate --status   # only show what is applied and what is pending

The application does the same at start-up, so running this by hand is only
needed to migrate before deploying, or to check a database. It never deletes
data. Migrations are defined in app/migrations.py.
"""
import argparse
import asyncio
import sys

from app.database import engine, init_db
from app.migrations import MIGRATIONS, applied_migrations


async def status() -> int:
    async with engine.begin() as conn:
        done = await applied_migrations(conn)
    for migration_id, _ in MIGRATIONS:
        print(f"{'applied' if migration_id in done else 'PENDING':<8} {migration_id}")
    return 0


async def migrate() -> int:
    newly_applied = await init_db()
    if newly_applied:
        print(f"Applied: {', '.join(newly_applied)}")
    else:
        print("Nothing to do: the database is up to date.")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m tools.migrate", description=__doc__.split("\n")[0])
    parser.add_argument("--status", action="store_true", help="show applied and pending migrations")
    args = parser.parse_args(argv)
    return asyncio.run(status() if args.status else migrate())


if __name__ == "__main__":
    sys.exit(main())
