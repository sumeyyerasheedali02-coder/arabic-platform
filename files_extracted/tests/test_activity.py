import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from app.routers import progress


@pytest.fixture
def activity_time(monkeypatch):
    class Clock:
        now = datetime(2026, 10, 15, 12)

        @classmethod
        def utcnow(cls):
            return cls.now

        @classmethod
        def advance(cls, seconds):
            cls.now += timedelta(seconds=seconds)

    monkeypatch.setattr(progress, "datetime", Clock)
    return Clock


async def ping(client, student, session, ms=0, lesson=None):
    return await client.post("/api/me/progress/activity", headers=student.headers,
                             json={"session_id": session, "active_ms": ms, "lesson_id": lesson})


async def test_activity_retries_do_not_duplicate_and_reading_does_not_complete_lesson(
    client, register, teacher, content, activity_time,
):
    student, staff = await register(), await teacher()
    session = str(uuid4())
    assert (await ping(client, student, session, lesson=content.a_muf)).status_code == 200
    activity_time.advance(20)
    assert (await ping(client, student, session, 19500, content.a_muf)).json()["recorded_ms"] == 19500
    activity_time.advance(10)
    await ping(client, student, session, 19500, content.a_muf)  # delivery retry
    await ping(client, student, session, 10000, content.a_muf)  # out-of-order delivery
    report = (await client.get(f"/api/teacher/students/{student.id}", headers=staff.headers)).json()
    assert report["student"]["active_time_sec"] == 19
    lesson = next(row for row in report["lessons"] if row["id"] == content.a_muf)
    assert lesson["time_spent_sec"] == 19
    assert lesson["status"] == "in_progress"
    assert not lesson["attempts"]
    assert report["student"]["lessons_done"] == 0
    assert (await client.get("/api/me/progress", headers=student.headers)).json() == []


async def test_server_caps_overlapping_tabs_and_fake_time(client, register, activity_time):
    student = await register()
    one, two = str(uuid4()), str(uuid4())
    await ping(client, student, one)
    await ping(client, student, two)
    activity_time.advance(15)
    assert (await ping(client, student, one, 15000)).json()["recorded_ms"] == 15000
    assert (await ping(client, student, two, 15000)).json()["recorded_ms"] == 0
    activity_time.advance(15)
    assert (await ping(client, student, one, 999999)).json()["recorded_ms"] == 30000


async def test_activity_requires_student_and_valid_fixed_lesson(client, register, teacher, content):
    assert (await client.post("/api/me/progress/activity", json={
        "session_id": str(uuid4()), "active_ms": 0})).status_code == 401
    staff, student = await teacher(), await register()
    assert (await ping(client, staff, str(uuid4()))).status_code == 403
    assert (await ping(client, student, str(uuid4()), lesson=999999)).status_code == 404
    assert (await ping(client, student, str(uuid4()), -1)).status_code == 422
    session = str(uuid4())
    await ping(client, student, session, lesson=content.a_muf)
    assert (await ping(client, student, session, lesson=content.a_hiwar)).status_code == 409


async def test_lesson_switch_and_account_isolation(client, register, teacher, content, activity_time):
    student, other, staff = await register(), await register(), await teacher()
    first, second = str(uuid4()), str(uuid4())
    await ping(client, student, first, lesson=content.a_muf)
    activity_time.advance(12)
    await ping(client, student, first, 12000, content.a_muf)
    await ping(client, student, second, lesson=content.a_hiwar)
    activity_time.advance(8)
    await ping(client, student, second, 8000, content.a_hiwar)
    await ping(client, other, first, 999999, content.a_muf)
    report = (await client.get(f"/api/teacher/students/{student.id}", headers=staff.headers)).json()
    times = {row["id"]: row["time_spent_sec"] for row in report["lessons"]}
    assert times[content.a_muf] == 12 and times[content.a_hiwar] == 8
    assert report["student"]["active_time_sec"] == 20


async def test_simultaneous_retries_are_counted_once(client, register, activity_time):
    student = await register()
    session = str(uuid4())
    await ping(client, student, session)
    activity_time.advance(15)
    replies = await asyncio.gather(*(ping(client, student, session, 15000) for _ in range(4)))
    assert all(reply.status_code == 200 for reply in replies)
    assert all(reply.json()["recorded_ms"] == 15000 for reply in replies)
