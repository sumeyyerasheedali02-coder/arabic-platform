async def test_teacher_endpoints_reject_guests_and_students(client, register):
    student = await register()
    for path in ("/api/teacher/students", "/api/teacher/units/stats"):
        assert (await client.get(path)).status_code == 401
        assert (await client.get(path, headers=student.headers)).status_code == 403


async def test_teacher_login_is_flagged(teacher):
    assert (await teacher()).body["is_teacher"] is True


async def test_student_summaries_report_points_and_completed_lessons(client, register, teacher, content):
    staff = await teacher()
    active, idle = await register(name="Aktif"), await register(name="Pasif")
    for exercise, answer in ((content.ex_choice, "kitap"), (content.ex_blank, "عليكم"),
                             (content.ex_true_false, "خطأ")):
        await client.post("/api/exercises/submit", headers=active.headers,
                          json={"exercise_id": exercise, "student_answer": answer})
    await client.post("/api/me/progress/update", headers=active.headers, params={
        "unit_id": content.unit_a, "lesson_id": content.a_muf, "score": 10, "status": "completed"})

    res = await client.get("/api/teacher/students", headers=staff.headers)
    assert res.status_code == 200
    rows = {row["student_id"]: row for row in res.json()}
    assert rows[active.id]["total_score"] == 20 and rows[active.id]["lessons_done"] == 1
    assert rows[active.id]["email"] == active.email and rows[active.id]["name"] == "Aktif"
    assert rows[idle.id]["total_score"] == 0 and rows[idle.id]["lessons_done"] == 0


async def test_unit_stats_cover_every_unit_in_order(client, teacher):
    staff = await teacher()
    stats = (await client.get("/api/teacher/units/stats", headers=staff.headers)).json()
    assert [row["unit_number"] for row in stats] == [1, 2]
    assert stats[0]["title_ar"] == "التَّحِيَّة"
    assert stats[0]["avg_score"] == 0 and stats[0]["completion_pct"] == 0


async def test_unit_completion_never_exceeds_100_percent(client, register, teacher, content):
    staff = await teacher()
    student = await register()
    for lesson in (content.a_hiwar, content.a_muf, content.a_nahw):
        await client.post("/api/me/progress/update", headers=student.headers, params={
            "unit_id": content.unit_a, "lesson_id": lesson, "score": 5, "status": "completed"})
    stats = (await client.get("/api/teacher/units/stats", headers=staff.headers)).json()
    # Two accounts (this student and the teacher), three lessons: 3 of 6 lesson completions.
    assert stats[0]["completion_pct"] == 50.0
    assert stats[1]["completion_pct"] == 0

    other = await register()
    for lesson in (content.a_hiwar, content.a_muf):
        await client.post("/api/me/progress/update", headers=other.headers, params={
            "unit_id": content.unit_a, "lesson_id": lesson, "score": 5, "status": "completed"})
    stats = (await client.get("/api/teacher/units/stats", headers=staff.headers)).json()
    assert stats[0]["completion_pct"] == 55.6       # 5 of 9
    assert stats[0]["avg_score"] == 5.0


def test_completion_percent_is_bounded():
    from app.services.reporting import completion_percent

    assert completion_percent(0, 10, 3) == 0
    assert completion_percent(30, 10, 3) == 100
    assert completion_percent(45, 10, 3) == 100      # duplicate rows cannot push it past 100
    assert completion_percent(5, 0, 3) == 0 and completion_percent(5, 10, 0) == 0
