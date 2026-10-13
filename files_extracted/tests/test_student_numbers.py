"""University numbers are distinct from database ids and can identify a login."""
import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.migrations import apply_migrations

from ._app import AsyncSessionLocal, engine, hash_password, models


@pytest.mark.parametrize("number", ["00123456", " 00123456 ", "٠٠١٢٣٤٥٦", "۰۰۱۲۳۴۵۶"])
async def test_number_normalization_persistence_email_and_number_login(
        client, register, login, teacher, number):
    student = await register(student_number=number)
    assert student.student_number == "00123456"
    for identifier in (student.email.upper(), number):
        response = await login(identifier, student.password)
        assert response.status_code == 200
        assert response.json()["student_id"] == student.id
        assert response.json()["student_number"] == "00123456"
    assert (await client.get("/api/auth/me", headers=student.headers)).json()["student_number"] == "00123456"
    staff = await teacher()
    rows = (await client.get("/api/teacher/students", headers=staff.headers)).json()
    assert rows[0]["student_number"] == "00123456"
    details = (await client.get(f"/api/teacher/students/{student.id}", headers=staff.headers)).json()
    assert details["student"]["student_number"] == "00123456"
    assert (await login("00123456", "wrong-password")).status_code == 401
    assert (await login("99999999", student.password)).status_code == 401


@pytest.mark.parametrize("number", [None, "", " ", "12a3", "12 34", "-123", "1" * 33, 123, True])
async def test_invalid_numbers_are_rejected(client, new_email, number):
    res = await client.post("/api/auth/register", json={
        "name": "Student", "email": new_email(), "password": "secret123",
        "class_section": "A", "student_number": number})
    assert res.status_code == 422


async def test_registration_requires_number(client, new_email):
    res = await client.post("/api/auth/register", json={
        "name": "Student", "email": new_email(), "password": "secret123", "class_section": "A"})
    assert res.status_code == 422


async def test_duplicate_number_cannot_create_a_second_account(client, register, new_email):
    await register(student_number="00123456")
    for number in ("00123456", "٠٠١٢٣٤٥٦"):
        email = new_email()
        res = await client.post("/api/auth/register", json={
            "name": "Other", "email": email, "password": "secret123",
            "class_section": "B", "student_number": number})
        assert res.status_code == 409
        assert (await client.get("/api/auth/check-email", params={"email": email})).json()["exists"] is False


async def old_account(login, content, section):
    async with AsyncSessionLocal() as db:
        account = models.Student(name="Old", email="old-number@example.com", class_section=section,
                                 password_hash=hash_password("secret123"))
        db.add(account)
        await db.flush()
        db.add(models.StudentProgress(student_id=account.id, lesson_id=content.a_muf,
                                      unit_id=content.unit_a, score=10, status="completed"))
        await db.commit()
    body = (await login(account.email, "secret123")).json()
    return account.id, {"Authorization": f"Bearer {body['access_token']}"}


@pytest.mark.parametrize("section", [None, "A"])
async def test_old_account_completes_missing_data_once_preserving_progress(client, login, content, section):
    sid, headers = await old_account(login, content, section)
    data = {"student_number": "00123456"} | ({"class_section": "B"} if section is None else {})
    res = await client.patch("/api/auth/me/profile", headers=headers, json=data)
    assert res.status_code == 200
    assert res.json()["student_number"] == "00123456"
    assert res.json()["class_section"] == (section or "B")
    assert (await client.patch("/api/auth/me/profile", headers=headers, json=data)).status_code == 200
    assert (await client.patch("/api/auth/me/profile", headers=headers,
                               json=data | {"student_number": "99999999"})).status_code == 409
    assert (await login("00123456", "secret123")).json()["student_id"] == sid
    assert (await client.get("/api/me/progress", headers=headers)).json()[0]["score"] == 10


async def test_duplicate_completion_does_not_partially_save_section(client, register, login, content):
    await register(student_number="00123456")
    sid, headers = await old_account(login, content, None)
    res = await client.patch("/api/auth/me/profile", headers=headers,
                             json={"student_number": "00123456", "class_section": "C"})
    assert res.status_code == 409
    async with AsyncSessionLocal() as db:
        account = await db.get(models.Student, sid)
        assert account.student_number is None and account.class_section is None
    res = await client.patch("/api/auth/me/profile", headers=headers,
                             json={"student_number": "00999999", "class_section": "C"})
    assert res.status_code == 200


async def test_profile_auth_ownership_and_section_protection(client, register, teacher, admin):
    data = {"student_number": "00123456", "class_section": "A"}
    assert (await client.patch("/api/auth/me/profile", json=data)).status_code == 401
    for staff in (await teacher(), await admin()):
        response = await client.patch("/api/auth/me/profile", headers=staff.headers, json=data)
        assert response.status_code == 403
    student = await register(student_number="00123456")
    other = await register(student_number="00999999")
    assert (await client.patch("/api/auth/me/profile", headers=student.headers,
                               json=data | {"class_section": "B"})).status_code == 409
    res = await client.patch("/api/auth/me/profile", headers=student.headers,
                             json=data | {"student_id": other.id})
    assert res.status_code == 200
    assert (await client.get("/api/auth/me", headers=other.headers)).json()["student_number"] == "00999999"


async def test_number_does_not_replace_database_id_or_allow_staff_login(client, teacher, login, register):
    student = await register(student_number="00001")
    assert (await login(str(student.id), student.password)).status_code == 401
    staff = await teacher()
    async with AsyncSessionLocal() as db:
        account = await db.get(models.Student, staff.id)
        account.student_number = "123456"
        await db.commit()
    assert (await login("123456", "teacher-pass-1")).status_code == 401
    assert (await login("teacher@example.com", "teacher-pass-1")).status_code == 200


async def test_number_migration_adds_nullable_unique_column_without_losing_data(client, register, content):
    student = await register(student_number="00123456")
    await client.post("/api/me/progress/update", headers=student.headers, params={
        "lesson_id": content.a_muf, "score": 10, "status": "completed"})
    async with engine.begin() as conn:
        await conn.execute(text("DROP INDEX ux_students_student_number"))
        await conn.execute(text("ALTER TABLE students DROP COLUMN student_number"))
        await conn.execute(text("DELETE FROM schema_migrations WHERE id = '0004_student_number'"))
        assert await apply_migrations(conn) == ["0004_student_number"]
        assert await apply_migrations(conn) == []
        assert (await conn.execute(text("SELECT student_number FROM students"))).scalar() is None
        assert (await conn.execute(text("SELECT score FROM student_progress"))).scalar() == 10
        await conn.execute(text("UPDATE students SET student_number = '00123456'"))
        with pytest.raises(IntegrityError):
            async with conn.begin_nested():
                await conn.execute(text(
                    "INSERT INTO students (name,email,password_hash,student_number) "
                    "VALUES ('Duplicate','duplicate@example.com','hash','00123456')"))
