"""Exercise management and section isolation through the real authentication dependencies."""
from datetime import datetime, timedelta

import pytest
from sqlalchemy import select, text

from app.config import ADMIN_EMAIL
from app.migrations import apply_migrations

from ._app import AsyncSessionLocal, engine, hash_password, models


def teacher_payload(email="new-teacher@example.com", sections=None):
    return {"name": "أستاذ جديد", "email": email, "password": "teacher-long-pass",
            "sections": sections if sections is not None else ["A", "B"]}


async def test_admin_identity_and_reserved_registration(client, admin):
    manager = await admin()
    assert manager.body["role"] == "admin" and manager.body["is_admin"] is True
    me = (await client.get("/api/auth/me", headers=manager.headers)).json()
    assert me["role"] == "admin" and me["is_teacher"] is True
    assert (await client.patch("/api/auth/me/section", headers=manager.headers,
                               json={"class_section": "C"})).status_code == 403
    for email in (ADMIN_EMAIL, ADMIN_EMAIL.upper()):
        res = await client.post("/api/auth/register", json={
            "name": "Fake", "email": email, "password": "secret123", "class_section": "A", "student_number": "00100001"})
        assert res.status_code == 403


async def test_admin_endpoints_deny_teachers_students_and_guests(client, teacher, register):
    staff = await teacher()
    student = await register()
    calls = [
        ("get", "/api/admin/teachers", None),
        ("post", "/api/admin/teachers", teacher_payload()),
        ("patch", f"/api/admin/teachers/{staff.id}", {"sections": ["A"], "is_active": True}),
        ("patch", f"/api/admin/students/{student.id}/section", {"class_section": "D"}),
    ]
    for method, path, payload in calls:
        kwargs = {"json": payload} if payload is not None else {}
        assert (await client.request(method, path, **kwargs)).status_code == 401
        for account in (staff, student):
            assert (await client.request(method, path, headers=account.headers, **kwargs)).status_code == 403


async def test_admin_creates_teachers_with_shared_sections_and_database_roles(client, admin, login):
    manager = await admin()
    for email in ("one@example.com", "two@example.com"):
        payload = teacher_payload(email, ["A", "A", "B"])
        payload["role"] = "admin"  # User-supplied role cannot grant admin access.
        created = await client.post("/api/admin/teachers", headers=manager.headers, json=payload)
        assert created.status_code == 201
        assert created.json()["sections"] == ["A", "B"]
        body = (await login(email, "teacher-long-pass")).json()
        assert body["role"] == "teacher" and body["is_admin"] is False and body["class_section"] is None
    rows = (await client.get("/api/admin/teachers", headers=manager.headers)).json()
    assert len(rows) == 2
    sections = (await client.get("/api/teacher/sections", headers=manager.headers)).json()
    assert sections[0]["teachers_count"] == 2
    assert (await client.post("/api/admin/teachers", headers=manager.headers,
                              json=teacher_payload("ONE@example.com"))).status_code == 409
    assert (await client.post("/api/admin/teachers", headers=manager.headers,
                              json=teacher_payload(ADMIN_EMAIL))).status_code == 409
    async with AsyncSessionLocal() as db:
        audits = (await db.execute(select(models.AdminAudit))).scalars().all()
        assert len(audits) == 2
        assert all("password" not in str(a.details) for a in audits)


@pytest.mark.parametrize("changes", [
    {"sections": []}, {"sections": ["E"]}, {"password": "short"},
    {"password": "ك" * 40}, {"name": "   "}, {"email": "invalid"},
])
async def test_teacher_creation_validation(client, admin, changes):
    manager = await admin()
    assert (await client.post("/api/admin/teachers", headers=manager.headers,
                              json=teacher_payload() | changes)).status_code == 422
    assert (await client.get("/api/admin/teachers", headers=manager.headers)).json() == []


async def test_reports_details_and_counts_are_limited_to_assigned_sections(
        client, admin, teacher, register, content):
    manager = await admin()
    staff = await teacher(sections=("A",))
    a, b = await register(class_section="A"), await register(class_section="B")
    for account in (a, b):
        await client.post("/api/exercises/submit", headers=account.headers,
                          json={"exercise_id": content.ex_choice, "student_answer": "kitap"})
        await client.post("/api/me/progress/update", headers=account.headers, params={
            "lesson_id": content.a_muf, "score": 10, "status": "completed"})
    rows = (await client.get("/api/teacher/students", headers=staff.headers)).json()
    assert [r["student_id"] for r in rows] == [a.id]
    assert rows[0]["accuracy_pct"] == 100 and rows[0]["completion_pct"] == 16.7
    stats = (await client.get("/api/teacher/units/stats", headers=staff.headers)).json()
    assert stats[0]["completion_pct"] == 33.3  # Only A's student is counted.
    sections = (await client.get("/api/teacher/sections", headers=staff.headers)).json()
    assert len(sections) == 1 and sections[0]["students_count"] == 1
    assert (await client.get(f"/api/teacher/students/{a.id}", headers=staff.headers)).status_code == 200
    for sid in (b.id, manager.id, 999999):
        assert (await client.get(f"/api/teacher/students/{sid}", headers=staff.headers)).status_code == 404
    for path in ("/api/teacher/students", "/api/teacher/units/stats"):
        assert (await client.get(path, headers=staff.headers, params={"section": "B"})).status_code == 403
        assert (await client.get(path, headers=staff.headers, params={"section": "E"})).status_code == 422
    all_rows = (await client.get("/api/teacher/students", headers=manager.headers)).json()
    assert {r["student_id"] for r in all_rows} == {a.id, b.id}


async def test_teacher_without_assignments_has_no_student_access(client, teacher, register):
    staff = await teacher(sections=())
    student = await register()
    assert (await client.get("/api/teacher/sections", headers=staff.headers)).json() == []
    assert (await client.get("/api/teacher/students", headers=staff.headers)).json() == []
    assert (await client.get(f"/api/teacher/students/{student.id}", headers=staff.headers)).status_code == 404


async def test_section_changes_take_effect_for_existing_tokens_without_losing_progress(
        client, admin, teacher, register, content):
    manager, staff = await admin(), await teacher(sections=("A",))
    student = await register()
    await client.post("/api/me/progress/update", headers=student.headers, params={
        "lesson_id": content.a_muf, "score": 10, "status": "completed"})
    res = await client.patch(f"/api/admin/students/{student.id}/section", headers=manager.headers,
                             json={"class_section": "B"})
    assert res.status_code == 200
    assert (await client.get(f"/api/teacher/students/{student.id}", headers=staff.headers)).status_code == 404
    assert (await client.get("/api/me/progress", headers=student.headers)).json()[0]["score"] == 10
    assert (await client.get("/api/auth/me", headers=student.headers)).json()["class_section"] == "B"
    saved = await client.patch(f"/api/admin/teachers/{staff.id}", headers=manager.headers,
                               json={"sections": ["B"], "is_active": True})
    assert saved.status_code == 200
    assert (await client.get(f"/api/teacher/students/{student.id}", headers=staff.headers)).status_code == 200
    assert (await client.patch(f"/api/admin/students/{staff.id}/section", headers=manager.headers,
                               json={"class_section": "D"})).status_code == 404


async def test_disable_and_password_reset_revoke_sessions(client, admin, teacher, login):
    manager, staff = await admin(), await teacher(sections=("A",))
    path = f"/api/admin/teachers/{staff.id}"
    assert (await client.patch(path, headers=manager.headers,
                               json={"sections": [], "is_active": True})).status_code == 422
    assert (await client.patch(path, headers=manager.headers,
                               json={"sections": ["A"], "is_active": False})).status_code == 200
    assert (await client.get("/api/teacher/students", headers=staff.headers)).status_code == 401
    assert (await login("teacher@example.com", "teacher-pass-1")).status_code == 401
    assert (await client.patch(path, headers=manager.headers, json={
        "sections": ["A"], "is_active": True, "password": "new-teacher-password"})).status_code == 200
    assert (await login("teacher@example.com", "teacher-pass-1")).status_code == 401
    body = (await login("teacher@example.com", "new-teacher-password")).json()
    assert body["role"] == "teacher"
    headers = {"Authorization": f"Bearer {body['access_token']}"}
    assert (await client.get("/api/teacher/students", headers=headers)).status_code == 200
    assert (await client.get("/api/teacher/students", headers=staff.headers)).status_code == 401
    assert (await client.patch(f"/api/admin/teachers/{manager.id}", headers=manager.headers,
                               json={"sections": [], "is_active": False})).status_code == 404


async def test_detail_has_history_errors_and_consistent_noninflated_points(
        client, admin, register, content):
    manager, student = await admin(), await register()
    async with AsyncSessionLocal() as db:
        account = await db.get(models.Student, student.id)
        account.last_login = datetime.utcnow() - timedelta(days=2)
        await db.commit()
    for answer in ("wrong", "kitap", "kitap"):
        await client.post("/api/exercises/submit", headers=student.headers,
                          json={"exercise_id": content.ex_choice, "student_answer": answer})
    detail = (await client.get(f"/api/teacher/students/{student.id}", headers=manager.headers)).json()
    summary = detail["student"]
    assert summary["total_score"] == 10 and summary["answers_count"] == 3
    assert summary["accuracy_pct"] == 66.7 and summary["correct_answers"] == 2
    assert datetime.fromisoformat(summary["last_active"]) > datetime.utcnow() - timedelta(hours=1)
    assert len(detail["lessons"]) == 6
    assert all(lesson["status"] == "not_started" for lesson in detail["lessons"])
    assert detail["history"][0]["answers"] == 3 and detail["history"][0]["correct"] == 2
    assert detail["recent_errors"][0]["student_answer"] == "wrong"
    assert (await client.get("/api/me/progress/summary", headers=student.headers)).json()["total_score"] == 10
    other = await register()
    assert (await client.get("/api/me/progress/summary", headers=other.headers)).json()["total_score"] == 0


async def test_staff_role_migration_preserves_accounts_and_activity(client, register, content):
    student = await register()
    await client.post("/api/me/progress/update", headers=student.headers, params={
        "lesson_id": content.a_muf, "score": 10, "status": "completed"})
    async with AsyncSessionLocal() as db:
        db.add_all([models.Student(name="Owner", email=ADMIN_EMAIL.upper(),
                                  password_hash=hash_password("owner-pass")),
                    models.Student(name="Legacy teacher", email="teacher@example.com", password_hash="hash")])
        await db.commit()
    async with engine.begin() as conn:
        await conn.execute(text("DROP INDEX ix_accounts_role_section"))
        for column in ("role", "is_active", "token_version"):
            await conn.execute(text(f"ALTER TABLE students DROP COLUMN {column}"))
        await conn.execute(text("DELETE FROM schema_migrations WHERE id = '0003_staff_roles'"))
        assert await apply_migrations(conn) == ["0003_staff_roles"]
        assert await apply_migrations(conn) == []
        roles = dict((await conn.execute(text("SELECT LOWER(email), role FROM students"))).all())
        assert roles[ADMIN_EMAIL] == "admin" and roles["teacher@example.com"] == "teacher"
        assert roles[student.email] == "student"
        assert (await conn.execute(text("SELECT score FROM student_progress"))).scalar() == 10
    me = (await client.get("/api/auth/me", headers=student.headers)).json()
    assert me["role"] == "student" and me["class_section"] == "A"


async def test_legacy_email_allowlist_does_not_grant_runtime_roles(client, login):
    async with AsyncSessionLocal() as db:
        db.add(models.Student(name="No rights", email="teacher@example.com",
                              password_hash=hash_password("secret123"), role="student"))
        await db.commit()
    body = (await login("teacher@example.com", "secret123")).json()
    assert body["is_teacher"] is False
    headers = {"Authorization": f"Bearer {body['access_token']}"}
    assert (await client.get("/api/teacher/students", headers=headers)).status_code == 403


async def test_owner_bootstrap_is_reserved_and_never_overwrites_existing_accounts(client, login):
    from tools.admin_account import create_owner

    assert await create_owner("Malek", "owner-recovery-pass") == 0
    body = (await login(ADMIN_EMAIL, "owner-recovery-pass")).json()
    assert body["is_admin"] is True and body["role"] == "admin"
    with pytest.raises(SystemExit):
        await create_owner("Other", "changed-password")
    assert (await login(ADMIN_EMAIL, "owner-recovery-pass")).status_code == 200
    assert (await login(ADMIN_EMAIL, "changed-password")).status_code == 401
