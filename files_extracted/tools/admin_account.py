"""Provision the designated owner when a deployment has no existing owner account.

    python -m tools.admin_account --name "Malek"

An existing account and its password are never overwritten. Existing owner
accounts are upgraded by migration 0003. The password is prompted privately.
"""
import argparse
import asyncio

from sqlalchemy import func, select

from app.config import ADMIN_EMAIL
from app.database import AsyncSessionLocal, init_db
from app.models import Student
from app.security import hash_password
from tools.teacher_accounts import _read_password


async def create_owner(name: str, password: str) -> int:
    await init_db()
    async with AsyncSessionLocal() as db:
        if (await db.execute(select(Student.id).where(func.lower(Student.email) == ADMIN_EMAIL))).first():
            raise SystemExit("Owner account already exists; no password or account was changed.")
        db.add(Student(name=name.strip() or "Malek", email=ADMIN_EMAIL,
                       password_hash=hash_password(password), role="admin"))
        await db.commit()
    print(f"Administrator created: {ADMIN_EMAIL}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--name", default="Malek")
    parser.add_argument("--password-env", metavar="VAR")
    args = parser.parse_args(argv)
    return asyncio.run(create_owner(args.name, _read_password(args.password_env)))


if __name__ == "__main__":
    raise SystemExit(main())
