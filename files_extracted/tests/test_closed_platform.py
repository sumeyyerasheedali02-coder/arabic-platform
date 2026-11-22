"""Only people who already have an account can enter: no guests, no new sign-ups."""
import dataclasses

import pytest

from app.config import get_settings
from app.routers import auth

from ._app import AsyncSessionLocal, models

SIGN_UP = {"name": "Yeni Öğrenci", "email": "new@example.com", "password": "secret123",
           "class_section": "A", "student_number": "0099999999"}

LEARNING_PATHS = ["/api/units", "/api/units/1", "/api/units/1/lessons", "/api/lessons/1",
                  "/api/units/1/vocabulary", "/api/vocabulary/search?q=a", "/api/lessons/1/dialogues",
                  "/api/units/1/exercises", "/api/shared-words", "/api/shared-words/units/1"]


@pytest.fixture
def close(monkeypatch):
    """Call it once the test has made the accounts it needs."""
    def _close():
        monkeypatch.setattr(auth, "get_settings",
                            lambda: dataclasses.replace(get_settings(), registration_open=False))
    return _close


async def students_count(db):
    from sqlalchemy import func, select
    return (await db.execute(select(func.count()).select_from(models.Student))).scalar_one()


async def test_registration_is_closed_by_default():
    from app.config import Settings
    assert Settings.__dataclass_fields__["registration_open"].default is False


async def test_nobody_new_can_sign_up_while_it_is_closed(client, close):
    close()
    async with AsyncSessionLocal() as db:
        before = await students_count(db)
    res = await client.post("/api/auth/register", json=SIGN_UP)
    assert res.status_code == 403
    async with AsyncSessionLocal() as db:
        assert await students_count(db) == before
    assert (await client.get("/api/auth/registration-status")).json() == {"open": False}


async def test_a_closed_platform_does_not_reveal_which_addresses_exist(client, register, close):
    known = await register()
    close()
    for email in (known.email, "stranger@example.com"):
        assert (await client.get("/api/auth/check-email", params={"email": email})).json()["exists"] is True


async def test_registered_accounts_still_log_in_while_it_is_closed(client, register, login, close):
    student = await register()
    close()
    assert (await login(student.email, student.password)).status_code == 200
    assert (await login(student.email, "wrong-password")).status_code == 401
    assert (await login("stranger@example.com", "secret123")).status_code == 401


async def test_sign_up_works_again_when_it_is_switched_on(client):
    assert (await client.get("/api/auth/registration-status")).json() == {"open": True}
    assert (await client.post("/api/auth/register", json=SIGN_UP)).status_code == 200


@pytest.mark.parametrize("path", LEARNING_PATHS)
async def test_learning_content_needs_a_login(client, path):
    assert (await client.get(path)).status_code == 401


async def test_exercises_cannot_be_answered_without_a_login(client, content):
    res = await client.post("/api/exercises/submit", json={"exercise_id": content.ex_choice, "answer": "kitap"})
    assert res.status_code == 401


async def test_students_teachers_and_admins_can_read_the_content(client, register, teacher, admin):
    for who in (await register(), await teacher(), await admin()):
        for path in ("/api/units", "/api/shared-words"):
            assert (await client.get(path, headers=who.headers)).status_code == 200
