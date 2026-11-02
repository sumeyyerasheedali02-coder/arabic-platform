"""A teacher or admin gives a student who forgot the password a temporary one."""
from app.routers.teacher import TEMPORARY_PASSWORD_LENGTH


def reset_path(student):
    return f"/api/teacher/students/{student.id}/reset-password"


async def test_teacher_resets_a_students_password(client, register, teacher, login):
    student = await register(password="forgotten-1")
    staff = await teacher(sections=("A",))

    res = await client.post(reset_path(student), headers=staff.headers)
    assert res.status_code == 200
    temporary = res.json()["temporary_password"]
    assert len(temporary) == TEMPORARY_PASSWORD_LENGTH and temporary.isalnum()
    assert res.headers["cache-control"] == "no-store"

    assert (await login(student.email, "forgotten-1")).status_code == 401
    assert (await login(student.email, temporary)).status_code == 200


async def test_reset_signs_the_student_out_everywhere(client, register, teacher):
    student = await register()
    staff = await teacher()
    assert (await client.get("/api/account/me", headers=student.headers)).status_code == 200

    await client.post(reset_path(student), headers=staff.headers)

    assert (await client.get("/api/account/me", headers=student.headers)).status_code == 401


async def test_each_reset_gives_a_different_password(client, register, teacher):
    student = await register()
    staff = await teacher()
    first = (await client.post(reset_path(student), headers=staff.headers)).json()["temporary_password"]
    second = (await client.post(reset_path(student), headers=staff.headers)).json()["temporary_password"]
    assert first != second


async def test_teacher_cannot_reset_a_student_of_another_section(client, register, teacher, login):
    student = await register(password="keep-this-1", class_section="A")
    staff = await teacher(sections=("B",))

    res = await client.post(reset_path(student), headers=staff.headers)

    assert res.status_code == 404
    assert (await login(student.email, "keep-this-1")).status_code == 200


async def test_students_and_guests_cannot_reset_passwords(client, register):
    victim, other = await register(), await register()
    assert (await client.post(reset_path(victim))).status_code == 401
    assert (await client.post(reset_path(victim), headers=other.headers)).status_code == 403


async def test_staff_accounts_are_not_reset_through_this_endpoint(client, teacher, admin):
    colleague = await teacher(email="colleague@example.com", sections=("A",))
    boss = await admin()
    res = await client.post(f"/api/teacher/students/{colleague.id}/reset-password", headers=boss.headers)
    assert res.status_code == 404


async def test_admin_can_reset_any_section_and_the_audit_never_holds_the_password(
        client, register, admin):
    student = await register(class_section="D")
    boss = await admin()

    res = await client.post(reset_path(student), headers=boss.headers)
    assert res.status_code == 200
    temporary = res.json()["temporary_password"]

    log = await client.get("/api/admin/audit", headers=boss.headers,
                           params={"action": "student_password_reset"})
    assert log.status_code == 200
    items = log.json()["items"]
    assert [i["action"] for i in items] == ["student_password_reset"]
    assert items[0]["target_id"] == student.id and items[0]["actor_name"] == "Malek"
    assert temporary not in log.text


async def test_unknown_student_is_not_found(client, teacher):
    staff = await teacher()
    assert (await client.post("/api/teacher/students/999999/reset-password",
                              headers=staff.headers)).status_code == 404
