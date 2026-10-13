"""Audit visibility and recent exercise results obey account and section boundaries."""
import pytest
from sqlalchemy import select

from ._app import AsyncSessionLocal, models


async def test_audit_requires_admin(client, admin, teacher, register):
    manager, staff, student = await admin(), await teacher(), await register()
    assert (await client.get("/api/admin/audit")).status_code == 401
    for account in (staff, student):
        assert (await client.get("/api/admin/audit", headers=account.headers)).status_code == 403
    assert (await client.get("/api/admin/audit", headers=manager.headers)).json() == {
        "total": 0, "items": []}


async def test_audit_order_pagination_filter_names_and_secret_exclusion(client, admin, register):
    manager, student = await admin(), await register()
    teacher = await client.post("/api/admin/teachers", headers=manager.headers, json={
        "name": "Teacher", "email": "audit-teacher@example.com",
        "password": "test-teacher-password", "sections": ["A"]})
    tid = teacher.json()["id"]
    await client.patch(f"/api/admin/teachers/{tid}", headers=manager.headers, json={
        "sections": ["B"], "is_active": True, "password": "new-teacher-password"})
    await client.patch(f"/api/admin/students/{student.id}/section", headers=manager.headers,
                       json={"class_section": "C"})
    # Defend the response boundary even if a historical row contains extra fields.
    async with AsyncSessionLocal() as db:
        row = (await db.execute(select(models.AdminAudit)
                                .where(models.AdminAudit.action == "teacher_created"))).scalar_one()
        row.details = row.details | {"password": "must-not-leak", "access_token": "must-not-leak"}
        await db.commit()
    first = (await client.get("/api/admin/audit", headers=manager.headers,
                              params={"limit": 2})).json()
    second = (await client.get("/api/admin/audit", headers=manager.headers,
                               params={"offset": 2, "limit": 2})).json()
    assert first["total"] == second["total"] == 3
    rows = first["items"] + second["items"]
    assert [r["action"] for r in rows] == [
        "student_section_changed", "teacher_updated", "teacher_created"]
    assert len({r["id"] for r in rows}) == 3
    assert all(r["actor_name"] == "Malek" for r in rows)
    assert rows[0]["target_id"] == student.id and rows[0]["target_role"] == "student"
    assert rows[1]["target_name"] == "Teacher" and rows[1]["details"]["password_reset"] is True
    assert "must-not-leak" not in str(rows)
    filtered = (await client.get("/api/admin/audit", headers=manager.headers,
                                 params={"action": "teacher_updated"})).json()
    assert filtered["total"] == 1 and filtered["items"][0]["action"] == "teacher_updated"


@pytest.mark.parametrize("params", [
    {"offset": -1}, {"limit": 0}, {"limit": 101}, {"action": "invalid"},
])
async def test_audit_validates_query_parameters(client, admin, params):
    manager = await admin()
    assert (await client.get("/api/admin/audit", headers=manager.headers, params=params)).status_code == 422


async def test_recent_results_are_ordered_and_scoped_to_assigned_students(
        client, admin, teacher, register, content):
    manager, staff = await admin(), await teacher(sections=("A",))
    a, b = await register(class_section="A"), await register(class_section="B")
    for student, answer in ((a, "wrong"), (b, "kitap"), (a, "kitap")):
        await client.post("/api/exercises/submit", headers=student.headers,
                          json={"exercise_id": content.ex_choice, "student_answer": answer})
    assert (await client.get("/api/teacher/activity")).status_code == 401
    assert (await client.get("/api/teacher/activity", headers=a.headers)).status_code == 403
    results = (await client.get("/api/teacher/activity", headers=staff.headers)).json()
    assert len(results) == 2 and {row["student_id"] for row in results} == {a.id}
    assert [row["is_correct"] for row in results] == [True, False]
    assert all(row["class_section"] == "A" for row in results)
    limited = (await client.get("/api/teacher/activity", headers=staff.headers,
                                params={"limit": 1})).json()
    assert limited == results[:1]
    assert (await client.get("/api/teacher/activity", headers=staff.headers,
                             params={"section": "B"})).status_code == 403
    assert (await client.get("/api/teacher/activity", headers=staff.headers,
                             params={"limit": 51})).status_code == 422
    all_results = (await client.get("/api/teacher/activity", headers=manager.headers)).json()
    assert len(all_results) == 3 and {row["student_id"] for row in all_results} == {a.id, b.id}
    b_results = (await client.get("/api/teacher/activity", headers=manager.headers,
                                 params={"section": "B"})).json()
    assert len(b_results) == 1 and b_results[0]["student_id"] == b.id


async def test_recent_results_empty_for_teacher_without_assignments(client, teacher, register, content):
    staff, student = await teacher(sections=()), await register()
    await client.post("/api/exercises/submit", headers=student.headers,
                      json={"exercise_id": content.ex_choice, "student_answer": "kitap"})
    assert (await client.get("/api/teacher/activity", headers=staff.headers)).json() == []
