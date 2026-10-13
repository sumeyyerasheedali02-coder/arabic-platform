"""Requests must not run a query per student, per unit or per word."""
from ._app import AsyncSessionLocal, models


async def _add_students(count, content, prefix):
    async with AsyncSessionLocal() as db:
        students = [models.Student(name=f"{prefix}{i}", email=f"{prefix}{i}@example.com",
                                   password_hash="not-a-real-hash", class_section="A") for i in range(count)]
        db.add_all(students)
        await db.flush()
        for s in students:
            db.add(models.StudentProgress(student_id=s.id, unit_id=content.unit_a, lesson_id=content.a_muf,
                                          status="completed", score=10, attempts=1))
            db.add(models.ExerciseAnswer(student_id=s.id, exercise_id=content.ex_choice,
                                         student_answer="kitap", is_correct=True, points_earned=10))
        await db.commit()


async def test_teacher_reports_use_a_fixed_number_of_queries(client, teacher, content, count_queries):
    staff = await teacher()
    counts = {}
    for label, extra in (("few", 3), ("many", 25)):
        await _add_students(extra, content, label)
        for path in ("/api/teacher/students", "/api/teacher/units/stats"):
            with count_queries() as counter:
                res = await client.get(path, headers=staff.headers)
            assert res.status_code == 200
            counts[(label, path)] = counter.count

    for path in ("/api/teacher/students", "/api/teacher/units/stats"):
        assert counts[("few", path)] == counts[("many", path)], counts
        assert counts[("many", path)] <= 6, counts

    rows = (await client.get("/api/teacher/students", headers=staff.headers)).json()
    assert len(rows) == 28                                  # teachers are excluded
    assert sum(row["total_score"] for row in rows) == 280 and sum(row["lessons_done"] for row in rows) == 28


async def test_adding_a_unit_to_review_does_not_query_per_word(client, register, content, count_queries):
    student = await register()
    with count_queries() as first:
        res = await client.post(f"/api/me/srs/add-unit/{content.unit_a}", headers=student.headers)
    assert res.json()["added"] == 4
    with count_queries() as again:
        res = await client.post(f"/api/me/srs/add-unit/{content.unit_a}", headers=student.headers)
    assert res.json()["added"] == 0
    # token check, words, existing cards, (insert) — the same for 4 words or 40
    assert first.count <= 4 and again.count <= 3

    partly = await register()
    await client.post("/api/me/srs/review", headers=partly.headers,
                      json={"vocabulary_id": content.vocab_a[0], "quality": 5})
    res = await client.post(f"/api/me/srs/add-unit/{content.unit_a}", headers=partly.headers)
    assert res.json()["added"] == 3
