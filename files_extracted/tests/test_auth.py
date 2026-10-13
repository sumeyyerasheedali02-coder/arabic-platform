from datetime import datetime, timedelta

import pytest
from jose import jwt
from sqlalchemy import delete

from ._app import TEACHER_EMAIL, TEST_SECRET, models


def _token(sub, minutes=5):
    payload = {"sub": sub, "exp": datetime.utcnow() + timedelta(minutes=minutes)}
    return {"Authorization": f"Bearer {jwt.encode(payload, TEST_SECRET, algorithm='HS256')}"}


async def test_register_returns_token_and_identity(register):
    student = await register(name="Mehmet Demir")
    assert student.body["token_type"] == "bearer"
    assert student.body["name"] == "Mehmet Demir"
    assert student.body["is_teacher"] is False
    assert isinstance(student.id, int)


async def test_register_rejects_duplicate_email(client, register):
    student = await register()
    res = await client.post("/api/auth/register", json={
        "name": "Other", "email": student.email, "password": "secret123"})
    assert res.status_code == 400


async def test_register_rejects_short_password(client, new_email):
    res = await client.post("/api/auth/register", json={
        "name": "A", "email": new_email(), "password": "12345"})
    assert res.status_code == 422


async def test_login_uses_form_encoding_and_returns_token(register, login):
    student = await register()
    res = await login(student.email, student.password)
    assert res.status_code == 200
    body = res.json()
    assert body["student_id"] == student.id and body["access_token"]


async def test_login_rejects_wrong_password_and_unknown_email(register, login, new_email):
    student = await register()
    assert (await login(student.email, "wrong-password")).status_code == 401
    assert (await login(new_email(), "secret123")).status_code == 401


async def test_check_email_reports_existence_without_revealing_name(client, register, new_email):
    student = await register(name="Gizli İsim")
    known = (await client.get("/api/auth/check-email", params={"email": student.email})).json()
    unknown = (await client.get("/api/auth/check-email", params={"email": new_email()})).json()
    assert known["exists"] is True and not known.get("name")
    assert unknown["exists"] is False


async def test_protected_endpoint_requires_valid_token(client):
    assert (await client.get("/api/me/progress")).status_code == 401
    bad = {"Authorization": "Bearer not-a-jwt"}
    assert (await client.get("/api/me/progress", headers=bad)).status_code == 401


async def test_expired_token_is_rejected(client, register):
    student = await register()
    assert (await client.get("/api/me/progress", headers=_token(str(student.id), -5))).status_code == 401


@pytest.mark.xfail(reason="non-numeric sub raises ValueError -> 500 instead of 401")
async def test_token_with_non_numeric_subject_is_rejected(client):
    assert (await client.get("/api/me/progress", headers=_token("abc"))).status_code == 401


@pytest.mark.xfail(reason="token of a deleted account is still accepted")
async def test_token_of_deleted_account_is_rejected(client, register, db):
    student = await register()
    await db.execute(delete(models.Student).where(models.Student.id == student.id))
    await db.commit()
    assert (await client.get("/api/me/progress", headers=student.headers)).status_code == 401


async def test_public_registration_cannot_claim_teacher_email(client):
    res = await client.post("/api/auth/register", json={
        "name": "Impostor", "email": TEACHER_EMAIL, "password": "secret123"})
    assert res.status_code == 403


async def test_case_variant_of_teacher_email_gains_nothing(client, teacher):
    await teacher()
    variant = TEACHER_EMAIL.replace("teacher", "Teacher")
    res = await client.post("/api/auth/register", json={
        "name": "Impostor", "email": variant, "password": "secret123"})
    assert res.status_code in (400, 403)


async def test_email_is_unique_regardless_of_case(client, register):
    student = await register(email="Mixed.Case@example.com")
    res = await client.post("/api/auth/register", json={
        "name": "Dup", "email": "mixed.case@example.com", "password": "secret123"})
    assert res.status_code == 400
    assert student.id


async def test_login_and_email_check_ignore_letter_case(client, register, login):
    student = await register(email="Fatma.Kaya@example.com")
    res = await login("FATMA.KAYA@example.com", student.password)
    assert res.status_code == 200 and res.json()["student_id"] == student.id
    check = await client.get("/api/auth/check-email", params={"email": "fatma.kaya@EXAMPLE.com"})
    assert check.json()["exists"] is True


async def test_teacher_account_is_provisioned_from_the_command_line(login):
    from tools import teacher_accounts

    assert await teacher_accounts.create_account(TEACHER_EMAIL.upper(), "Hoca", "long-teacher-pass") == 0
    res = await login(TEACHER_EMAIL, "long-teacher-pass")
    assert res.status_code == 200 and res.json()["is_teacher"] is True

    with pytest.raises(SystemExit):   # already exists
        await teacher_accounts.create_account(TEACHER_EMAIL, "Hoca", "long-teacher-pass")
    with pytest.raises(SystemExit):   # not on the allowlist
        await teacher_accounts.create_account("someone@example.com", "X", "long-teacher-pass")

    assert await teacher_accounts.set_password(TEACHER_EMAIL, "another-long-pass") == 0
    assert (await login(TEACHER_EMAIL, "long-teacher-pass")).status_code == 401
    assert (await login(TEACHER_EMAIL, "another-long-pass")).status_code == 200
