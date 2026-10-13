"""Provision and review teacher accounts.

Teacher rights belong to accounts whose e-mail is listed in TEACHER_EMAILS.
Those addresses cannot be registered through the public sign-up form (the
platform does not verify e-mail ownership), so the account is created here by
whoever operates the server.

    python -m tools.teacher_accounts list
    python -m tools.teacher_accounts create --email teacher@karabuk.edu.tr --name "Ad Soyad"
    python -m tools.teacher_accounts set-password --email teacher@karabuk.edu.tr

The password is asked for interactively. For non-interactive use, put it in an
environment variable and pass its name with --password-env.
"""
import argparse
import asyncio
import getpass
import os
import sys

from sqlalchemy import func, select

from auth import TEACHER_EMAILS, hash_password, is_teacher_email
from database import AsyncSessionLocal, Student, init_db

MIN_PASSWORD_LENGTH = 10


def _read_password(env_name: str | None) -> str:
    if env_name:
        password = os.environ.get(env_name, "")
        if not password:
            raise SystemExit(f"environment variable {env_name} is empty or not set")
    else:
        password = getpass.getpass("Password: ")
        if password != getpass.getpass("Repeat password: "):
            raise SystemExit("the two passwords do not match")
    if len(password) < MIN_PASSWORD_LENGTH:
        raise SystemExit(f"use at least {MIN_PASSWORD_LENGTH} characters for a teacher password")
    if len(password.encode("utf-8")) > 72:
        raise SystemExit("the password is too long (bcrypt accepts at most 72 bytes)")
    return password


async def _accounts_for(db, email: str) -> list[Student]:
    result = await db.execute(
        select(Student).where(func.lower(Student.email) == email.lower()).order_by(Student.id))
    return list(result.scalars().all())


async def list_accounts() -> int:
    if not TEACHER_EMAILS:
        print("TEACHER_EMAILS is empty: no account has teacher rights.")
        return 0
    await init_db()
    problems = 0
    async with AsyncSessionLocal() as db:
        for email in sorted(TEACHER_EMAILS):
            accounts = await _accounts_for(db, email)
            if not accounts:
                print(f"{email}: no account yet (create one with the `create` command)")
            for account in accounts:
                print(f"{email}: id={account.id} stored_as={account.email} name={account.name!r} "
                      f"created={account.created_at} last_login={account.last_login}")
            if len(accounts) > 1:
                problems += 1
                print(f"  WARNING: {len(accounts)} accounts share this address in different "
                      "letter case; only the lowest id can log in. Review and delete the others.")
    print("\nAccounts created before this safeguard existed were not verified. If you are "
          "not sure who registered one, reset it with `set-password`.")
    return 1 if problems else 0


async def create_account(email: str, name: str, password: str) -> int:
    email = email.strip().lower()
    if not is_teacher_email(email):
        raise SystemExit(f"{email} is not listed in TEACHER_EMAILS; add it there first")
    await init_db()
    async with AsyncSessionLocal() as db:
        if await _accounts_for(db, email):
            raise SystemExit(f"an account for {email} already exists; use `set-password` instead")
        db.add(Student(name=name, email=email, password_hash=hash_password(password)))
        await db.commit()
    print(f"Teacher account created for {email}.")
    return 0


async def set_password(email: str, password: str) -> int:
    email = email.strip().lower()
    if not is_teacher_email(email):
        raise SystemExit(f"{email} is not listed in TEACHER_EMAILS")
    await init_db()
    async with AsyncSessionLocal() as db:
        accounts = await _accounts_for(db, email)
        if not accounts:
            raise SystemExit(f"no account for {email}; use `create` instead")
        accounts[0].password_hash = hash_password(password)
        await db.commit()
    print(f"Password updated for {email} (account id {accounts[0].id}).")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="show every account that has teacher rights")
    for name, text in (("create", "create the account for an allowlisted address"),
                       ("set-password", "set a new password for an existing teacher account")):
        sub = commands.add_parser(name, help=text)
        sub.add_argument("--email", required=True)
        sub.add_argument("--password-env", metavar="VAR",
                         help="read the password from this environment variable")
        if name == "create":
            sub.add_argument("--name", required=True)
    args = parser.parse_args(argv)

    if args.command == "list":
        return asyncio.run(list_accounts())
    password = _read_password(args.password_env)
    if args.command == "create":
        return asyncio.run(create_account(args.email, args.name, password))
    return asyncio.run(set_password(args.email, password))


if __name__ == "__main__":
    sys.exit(main())
