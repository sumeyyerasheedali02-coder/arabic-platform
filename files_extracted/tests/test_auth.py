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
        "name": "Other", "email": student.email, "password": "secret123", "class_section": "A", "student_number": "00100001"})
    assert res.status_code == 400


async def test_register_rejects_short_password(client, new_email):
    res = await client.post("/api/auth/register", json={
        "name": "A", "email": new_email(), "password": "12345", "class_section": "A", "student_number": "00100001"})
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


async def test_token_with_non_numeric_subject_is_rejected(client):
    assert (await client.get("/api/me/progress", headers=_token("abc"))).status_code == 401


async def test_token_of_deleted_account_is_rejected(client, register, db):
    student = await register()
    await db.execute(delete(models.Student).where(models.Student.id == student.id))
    await db.commit()
    assert (await client.get("/api/me/progress", headers=student.headers)).status_code == 401


async def test_public_registration_cannot_claim_teacher_email(client):
    res = await client.post("/api/auth/register", json={
        "name": "Impostor", "email": TEACHER_EMAIL, "password": "secret123", "class_section": "A", "student_number": "00100001"})
    assert res.status_code == 403


async def test_case_variant_of_teacher_email_gains_nothing(client, teacher):
    await teacher()
    variant = TEACHER_EMAIL.replace("teacher", "Teacher")
    res = await client.post("/api/auth/register", json={
        "name": "Impostor", "email": variant, "password": "secret123", "class_section": "A", "student_number": "00100001"})
    assert res.status_code in (400, 403)


async def test_email_is_unique_regardless_of_case(client, register):
    student = await register(email="Mixed.Case@example.com")
    res = await client.post("/api/auth/register", json={
        "name": "Dup", "email": "mixed.case@example.com", "password": "secret123", "class_section": "A", "student_number": "00100001"})
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


async def test_token_without_subject_is_rejected(client):
    from jose import jwt as jose_jwt
    token = jose_jwt.encode({"exp": datetime.utcnow() + timedelta(minutes=5)}, TEST_SECRET, algorithm="HS256")
    res = await client.get("/api/me/progress", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 401


async def test_session_endpoint_describes_the_logged_in_account(client, register, teacher):
    student = await register(name="Zeynep Arslan")
    me = await client.get("/api/auth/me", headers=student.headers)
    assert me.json() == {"student_id": student.id, "name": "Zeynep Arslan",
                         "is_teacher": False, "class_section": "A", "role": "student", "is_admin": False,
                         "student_number": student.student_number}

    staff = await teacher()
    assert (await client.get("/api/auth/me", headers=staff.headers)).json()["is_teacher"] is True
    assert (await client.get("/api/auth/me")).status_code == 401


async def test_password_longer_than_bcrypt_accepts_is_rejected_not_a_server_error(
        client, new_email, register, login):
    too_long = "ك" * 40          # 80 bytes in UTF-8
    res = await client.post("/api/auth/register", json={
        "name": "Uzun", "email": new_email(), "password": too_long, "class_section": "A", "student_number": "00100001"})
    assert res.status_code == 422

    student = await register()
    assert (await login(student.email, too_long)).status_code == 401


async def test_repeated_failed_logins_lock_that_identifier_only(register, login, monkeypatch):
    from app.routers import auth

    monkeypatch.setattr(auth, "FAILED_LOGINS_PER_ACCOUNT", 3)
    target, other = await register(), await register()
    for _ in range(3):
        assert (await login(target.email.upper(), "wrong-password")).status_code == 401
    # Locked even with the right password, whatever the spelling of the address.
    assert (await login(target.email, target.password)).status_code == 429
    assert (await login(f"  {target.email}  ", "wrong-password")).status_code == 429
    assert (await login(other.email, other.password)).status_code == 200


async def test_failed_logins_from_one_address_are_limited(register, login, new_email, monkeypatch):
    from app.routers import auth

    monkeypatch.setattr(auth, "known_client_ip", lambda request: "203.0.113.9")
    monkeypatch.setattr(auth, "FAILED_LOGINS_PER_ADDRESS", 4)
    student = await register()
    for _ in range(4):
        assert (await login(new_email(), "wrong-password")).status_code == 401
    assert (await login(student.email, student.password)).status_code == 429


async def test_unknown_addresses_never_lock_out_other_accounts(register, login, new_email, monkeypatch):
    """Behind a proxy without CLIENT_IP_HEADER every request has the same address."""
    from app.routers import auth

    monkeypatch.setattr(auth, "FAILED_LOGINS_PER_ADDRESS", 4)
    student = await register()
    for _ in range(10):
        assert (await login(new_email(), "wrong-password")).status_code == 401
    assert (await login(student.email, student.password)).status_code == 200


async def test_successful_logins_are_not_limited(register, login):
    student = await register()
    for _ in range(15):
        assert (await login(student.email, student.password)).status_code == 200


async def test_student_number_spellings_share_one_failure_count(register, login, monkeypatch):
    from app.routers import auth

    monkeypatch.setattr(auth, "FAILED_LOGINS_PER_ACCOUNT", 2)
    student = await register(student_number="12345")
    assert (await login("12345", "wrong-password")).status_code == 401
    assert (await login("١٢٣٤٥", "wrong-password")).status_code == 401
    assert (await login("12345", student.password)).status_code == 429
