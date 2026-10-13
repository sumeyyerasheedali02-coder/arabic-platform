"""Real login, scope enforcement, publication, arithmetic, and multi-teacher conflicts."""
import pytest
from sqlalchemy import select, update

from app.models import Student, TeacherSection
from app.tracking.calculations import overall_result, term_result, weekly_total
from app.tracking.models import TrackingAudit, TrackingCycle, TrackingEntry


async def create(client, headers, section="A", year="2026-2027"):
    response = await client.post("/api/tracking/cycles", headers=headers,
                                 json={"section": section, "academic_year": year})
    assert response.status_code == 201, response.text
    return response.json()["id"]


async def state(client, headers, cycle):
    response = await client.get(f"/api/tracking/cycles/{cycle}/state", headers=headers)
    assert response.status_code == 200, response.text
    return response.json()


async def week(client, headers, cycle, number=1):
    snapshot = await state(client, headers, cycle)
    response = await client.post(f"/api/tracking/cycles/{cycle}/weeks", headers=headers, json={
        "revision": snapshot["cycle"]["revision"], "number": number, "starts_on": "2026-10-12"})
    assert response.status_code == 201, response.text
    return response.json()["week_id"]


def grades(student_id, score=10):
    return {"student_id": student_id, "writing": score, "class_activity": score,
            "home_activity": score, "language_lab": score, "note": "ملاحظة <script>"}


async def save(client, headers, cycle, week_id, entries, *, publish=False, revision=None):
    if revision is None:
        revision = (await state(client, headers, cycle))["cycle"]["revision"]
    return await client.put(f"/api/tracking/cycles/{cycle}/weeks/{week_id}", headers=headers,
                            json={"revision": revision, "entries": entries, "publish": publish})


async def term(client, headers, cycle, number, first, last, entries, *, publish=False):
    revision = (await state(client, headers, cycle))["cycle"]["revision"]
    return await client.put(f"/api/tracking/cycles/{cycle}/terms/{number}", headers=headers, json={
        "revision": revision, "first_week": first, "last_week": last,
        "entries": entries, "publish": publish})


def test_missing_and_zero_and_complete_term_arithmetic():
    assert weekly_total(grades(1, 0)) == 0
    assert weekly_total({**grades(1), "writing": None}) is None
    config = {"first_week": 1, "last_week": 2, "published": True}
    weeks = [{"id": 1, "number": 1, "published": True}, {"id": 2, "number": 2, "published": True}]
    entries = {1: grades(1, 10), 2: grades(1, 0)}
    result = term_result(config, weeks, entries, 30, published_only=True)
    assert result == {"activity": 20, "exam": 30, "total": 50}
    assert overall_result([result, result]) == {"score": 50, "passed": True, "needed": 0}
    assert term_result(config, weeks[:1], entries, 60) is None
    assert term_result(config, weeks, {1: entries[1]}, 60) is None
    assert term_result(config, [{**w, "published": False} for w in weeks], entries, 60,
                       published_only=True) is None


async def test_same_account_login_by_number_and_section_scope(client, register, teacher, admin):
    student = await register(class_section="A", student_number="0000741")
    other = await register(class_section="B")
    first = await teacher(sections=("A",), email="first@example.com")
    second = await teacher(sections=("A",), email="second@example.com")
    administrator = await admin()
    cycle = await create(client, first.headers)
    login = await client.post("/api/auth/login", data={"username": "0000741", "password": student.password})
    assert login.status_code == 200
    assert login.json()["student_id"] == student.id
    for headers in (first.headers, second.headers, administrator.headers):
        snapshot = await state(client, headers, cycle)
        assert [s["id"] for s in snapshot["students"]] == [student.id]
    assert (await client.get(f"/api/tracking/cycles/{cycle}/state", headers=student.headers)).status_code == 403
    assert (await client.get(f"/api/tracking/cycles/{cycle}/me", headers=other.headers)).status_code == 403
    assert (await client.post("/api/tracking/cycles", headers=first.headers,
                             json={"section": "B", "academic_year": "2026-2027"})).status_code == 403
    assert (await client.get("/api/tracking/cycles")).status_code == 401


async def test_drafts_and_notes_are_private_until_publish(client, register, teacher):
    student = await register()
    sibling = await register()
    staff = await teacher()
    cycle = await create(client, staff.headers)
    w = await week(client, staff.headers, cycle)
    assert (await save(client, staff.headers, cycle, w, [grades(student.id), grades(sibling.id, 0)])).status_code == 200
    response = await client.get(f"/api/tracking/cycles/{cycle}/me", headers=student.headers)
    assert response.json()["entries"] == []
    assert response.json()["weeks"] == []
    assert "exams" not in response.json() and "terms" not in response.json()
    assert (await save(client, staff.headers, cycle, w, [grades(student.id), grades(sibling.id, 0)], publish=True)).status_code == 200
    body = (await client.get(f"/api/tracking/cycles/{cycle}/me", headers=student.headers)).json()
    assert len(body["entries"]) == 1 and body["entries"][0]["student_id"] == student.id
    assert body["entries"][0]["note"] == "ملاحظة <script>"
    assert len(body["students"]) == 1
    assert "audit" not in body


async def test_out_of_section_grade_injection_and_duplicates_roll_back(client, register, teacher, db):
    a, b = await register(class_section="A"), await register(class_section="B")
    staff = await teacher(sections=("A",))
    cycle = await create(client, staff.headers)
    w = await week(client, staff.headers, cycle)
    before = await state(client, staff.headers, cycle)
    response = await save(client, staff.headers, cycle, w, [grades(a.id), grades(b.id)])
    assert response.status_code == 403
    assert (await state(client, staff.headers, cycle))["cycle"]["revision"] == before["cycle"]["revision"]
    assert (await db.execute(select(TrackingEntry))).scalars().all() == []
    assert (await save(client, staff.headers, cycle, w, [grades(a.id), grades(a.id)])).status_code == 422


@pytest.mark.parametrize("bad", [-1, 10.1, "NaN", "Infinity"])
async def test_invalid_weekly_marks_rejected(client, register, teacher, bad):
    student = await register()
    staff = await teacher()
    cycle = await create(client, staff.headers)
    w = await week(client, staff.headers, cycle)
    assert (await save(client, staff.headers, cycle, w, [{**grades(student.id), "writing": bad}])).status_code == 422


async def test_multi_teacher_stale_revision_cannot_overwrite(client, register, teacher):
    student = await register()
    one = await teacher(email="one@example.com")
    two = await teacher(email="two@example.com")
    cycle = await create(client, one.headers)
    w = await week(client, one.headers, cycle)
    revision = (await state(client, one.headers, cycle))["cycle"]["revision"]
    assert (await save(client, one.headers, cycle, w, [grades(student.id, 8)], revision=revision)).status_code == 200
    assert (await save(client, two.headers, cycle, w, [grades(student.id, 1)], revision=revision)).status_code == 409
    assert (await state(client, two.headers, cycle))["entries"][0]["writing"] == 8


async def test_incomplete_publication_rolls_back_all_changes(client, register, teacher):
    student = await register()
    await register()
    staff = await teacher()
    cycle = await create(client, staff.headers)
    w = await week(client, staff.headers, cycle)
    before = await state(client, staff.headers, cycle)
    assert (await save(client, staff.headers, cycle, w, [grades(student.id)], publish=True)).status_code == 422
    after = await state(client, staff.headers, cycle)
    assert after["cycle"]["revision"] == before["cycle"]["revision"]
    assert after["entries"] == []


async def test_terms_final_and_reediting_invalidates_publication(client, register, teacher):
    student = await register()
    staff = await teacher()
    cycle = await create(client, staff.headers)
    w1 = await week(client, staff.headers, cycle)
    w2 = await week(client, staff.headers, cycle, 2)
    for w, score in ((w1, 10), (w2, 5)):
        assert (await save(client, staff.headers, cycle, w, [grades(student.id, score)], publish=True)).status_code == 200
    assert (await term(client, staff.headers, cycle, 1, 1, 1,
                       [{"student_id": student.id, "score": 60}], publish=True)).status_code == 200
    assert (await term(client, staff.headers, cycle, 2, 2, 2,
                       [{"student_id": student.id, "score": 0}], publish=True)).status_code == 200
    revision = (await state(client, staff.headers, cycle))["cycle"]["revision"]
    assert (await client.patch(f"/api/tracking/cycles/{cycle}/final-publication", headers=staff.headers,
                              json={"revision": revision, "published": True})).status_code == 200
    result = (await client.get(f"/api/tracking/cycles/{cycle}/me", headers=student.headers)).json()["results"]
    assert result["terms"][0]["total"] == 100 and result["terms"][1]["total"] == 20
    assert result["overall"]["score"] == 60
    assert (await save(client, staff.headers, cycle, w1, [grades(student.id, 0)])).status_code == 200
    data = (await client.get(f"/api/tracking/cycles/{cycle}/me", headers=student.headers)).json()
    assert len(data["entries"]) == 1
    assert data["results"]["terms"][0] is None and data["results"]["overall"] is None


async def test_missing_weeks_overlapping_terms_and_out_of_range_exams(client, register, teacher):
    student = await register()
    staff = await teacher()
    cycle = await create(client, staff.headers)
    await week(client, staff.headers, cycle)
    entry = [{"student_id": student.id, "score": 40}]
    assert (await term(client, staff.headers, cycle, 1, 1, 2, entry, publish=True)).status_code == 422
    assert (await term(client, staff.headers, cycle, 1, 1, 2, entry)).status_code == 200
    assert (await term(client, staff.headers, cycle, 2, 2, 4, entry)).status_code == 422
    assert (await term(client, staff.headers, cycle, 2, 3, 4, [{"student_id": student.id, "score": 61}])).status_code == 422


async def test_revoked_assignments_and_disabled_account_are_effective(client, register, teacher, db):
    student = await register()
    staff = await teacher(sections=("A",))
    cycle = await create(client, staff.headers)
    await db.execute(TeacherSection.__table__.delete().where(TeacherSection.teacher_id == staff.id))
    await db.commit()
    assert (await client.get(f"/api/tracking/cycles/{cycle}/state", headers=staff.headers)).status_code == 403
    await db.execute(update(Student).where(Student.id == student.id).values(is_active=False))
    await db.commit()
    assert (await client.get("/api/tracking/cycles", headers=student.headers)).status_code == 401


async def test_years_are_separate_and_audit_retains_actor(client, register, teacher, db):
    student = await register()
    staff = await teacher()
    first = await create(client, staff.headers)
    second = await create(client, staff.headers, year="2027-2028")
    w = await week(client, staff.headers, first)
    await save(client, staff.headers, first, w, [grades(student.id, 8)])
    assert (await state(client, staff.headers, second))["entries"] == []
    logs = (await db.execute(select(TrackingAudit).where(TrackingAudit.action == "week_saved"))).scalars().all()
    assert len(logs) == 1 and logs[0].actor_id == staff.id
    assert logs[0].details["changes"][0]["after"]["writing"] == 8
    assert (await db.execute(select(TrackingCycle))).scalars().all()


async def test_foreign_week_id_cannot_be_used_in_another_cycle(client, register, teacher):
    student = await register()
    staff = await teacher()
    a, b = await create(client, staff.headers), await create(client, staff.headers, section="B")
    foreign_week = await week(client, staff.headers, b)
    assert (await save(client, staff.headers, a, foreign_week, [grades(student.id)])).status_code == 404
