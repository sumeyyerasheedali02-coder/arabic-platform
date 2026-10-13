from sqlalchemy import func, select

from ._app import models


async def test_submit_requires_login(client, content):
    res = await client.post("/api/exercises/submit", json={
        "exercise_id": content.ex_choice, "student_answer": "kitap"})
    assert res.status_code == 401


async def test_correct_answer_earns_the_exercise_points(client, register, content):
    student = await register()
    res = await client.post("/api/exercises/submit", headers=student.headers, json={
        "exercise_id": content.ex_choice, "student_answer": "kitap"})
    assert res.status_code == 200
    assert res.json() == {"is_correct": True, "correct_answer": "kitap",
                          "explanation_ar": None, "points_earned": 10}


async def test_answer_check_ignores_diacritics_case_and_outer_spaces(client, register, content):
    student = await register()
    plain = await client.post("/api/exercises/submit", headers=student.headers, json={
        "exercise_id": content.ex_blank, "student_answer": "  عليكم "})
    assert plain.json()["is_correct"] is True
    upper = await client.post("/api/exercises/submit", headers=student.headers, json={
        "exercise_id": content.ex_choice, "student_answer": "KITAP"})
    assert upper.json()["is_correct"] is True


async def test_wrong_answer_earns_nothing_and_reveals_solution(client, register, content):
    student = await register()
    res = await client.post("/api/exercises/submit", headers=student.headers, json={
        "exercise_id": content.ex_blank, "student_answer": "شكرا"})
    assert res.json() == {"is_correct": False, "correct_answer": "عَلَيْكُم",
                          "explanation_ar": "رد التحية", "points_earned": 0}


async def test_every_attempt_is_recorded(client, register, content, db):
    student = await register()
    for answer in ("kalem", "kitap"):
        await client.post("/api/exercises/submit", headers=student.headers, json={
            "exercise_id": content.ex_choice, "student_answer": answer})
    recorded = (await db.execute(
        select(func.count(models.ExerciseAnswer.id))
        .where(models.ExerciseAnswer.student_id == student.id))).scalar()
    assert recorded == 2


async def test_unknown_exercise_is_404(client, register):
    student = await register()
    res = await client.post("/api/exercises/submit", headers=student.headers, json={
        "exercise_id": 99999, "student_answer": "x"})
    assert res.status_code == 404
