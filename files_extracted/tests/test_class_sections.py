"""Real section selection: persistence, validation, old accounts and authorization."""
import pytest
from sqlalchemy import select

from ._app import AsyncSessionLocal, hash_password, models


@pytest.mark.parametrize("section", ["A", "B", "C", "D", " b "])
async def test_registration_saves_section_in_login_session_and_teacher_report(
        client, register, login, teacher, section):
    student = await register(class_section=section)
    expected = section.strip().upper()
    assert student.body["class_section"] == expected
    assert (await login(student.email, student.password)).json()["class_section"] == expected
    assert (await client.get("/api/auth/me", headers=student.headers)).json()["class_section"] == expected
    async with AsyncSessionLocal() as db:
        account = await db.get(models.Student, student.id)
        assert account.class_section == expected and account.year == 1
    staff = await teacher()
    rows = (await client.get("/api/teacher/students", headers=staff.headers)).json()
    assert next(row for row in rows if row["student_id"] == student.id)["class_section"] == expected


@pytest.mark.parametrize("section", [None, "", "E", "AB", 1])
async def test_registration_rejects_invalid_section(client, new_email, section):
    email = new_email()
    response = await client.post("/api/auth/register", json={
        "name": "Student", "email": email, "password": "secret123", "class_section": section,
        "student_number": "00100001"})
    assert response.status_code == 422
    assert (await client.get("/api/auth/check-email", params={"email": email})).json()["exists"] is False


async def test_registration_requires_an_explicit_section(client, new_email):
    response = await client.post("/api/auth/register", json={
        "name": "Student", "email": new_email(), "password": "secret123", "year": 4,
        "student_number": "00100001"})
    assert response.status_code == 422


async def test_existing_student_can_choose_once_without_losing_progress(client, login, content):
    async with AsyncSessionLocal() as db:
        account = models.Student(name="Existing", email="old@example.com",
                                 password_hash=hash_password("secret123"), year=3)
        db.add(account)
        await db.flush()
        db.add(models.StudentProgress(student_id=account.id, unit_id=content.unit_a,
                                      lesson_id=content.a_muf, status="completed", score=10))
        await db.commit()
        student_id = account.id
    body = (await login("old@example.com", "secret123")).json()
    assert body["class_section"] is None
    headers = {"Authorization": f"Bearer {body['access_token']}"}
    saved = await client.patch("/api/auth/me/section", headers=headers, json={"class_section": "C"})
    assert saved.status_code == 200 and saved.json()["class_section"] == "C"
    # Repeating the same choice is safe; a later request cannot change it.
    assert (await client.patch("/api/auth/me/section", headers=headers,
                               json={"class_section": "C"})).status_code == 200
    assert (await client.patch("/api/auth/me/section", headers=headers,
                               json={"class_section": "D"})).status_code == 409
    assert (await login("old@example.com", "secret123")).json()["class_section"] == "C"
    assert (await client.get("/api/me/progress", headers=headers)).json()[0]["score"] == 10
    async with AsyncSessionLocal() as db:
        account = await db.get(models.Student, student_id)
        assert account.year == 1


async def test_section_choice_requires_student_auth_and_cannot_target_someone_else(
        client, register, teacher):
    payload = {"class_section": "D"}
    assert (await client.patch("/api/auth/me/section", json=payload)).status_code == 401
    staff = await teacher()
    response = await client.patch("/api/auth/me/section", headers=staff.headers, json=payload)
    assert response.status_code == 403
    first, other = await register(class_section="A"), await register(class_section="B")
    response = await client.patch("/api/auth/me/section", headers=first.headers,
                                  json={"class_section": "A", "student_id": other.id})
    assert response.status_code == 200
    async with AsyncSessionLocal() as db:
        assert (await db.get(models.Student, other.id)).class_section == "B"


async def test_section_choice_rejects_invalid_values(client, register):
    student = await register()
    response = await client.patch("/api/auth/me/section", headers=student.headers,
                                  json={"class_section": "E"})
    assert response.status_code == 422
    async with AsyncSessionLocal() as db:
        assert (await db.execute(select(models.Student.class_section)
                                 .where(models.Student.id == student.id))).scalar_one() == "A"
