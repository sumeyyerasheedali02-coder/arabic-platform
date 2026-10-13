def _update(client, headers, **params):
    return client.post("/api/me/progress/update", headers=headers, params=params)


async def test_progress_requires_login(client, content):
    assert (await client.get("/api/me/progress")).status_code == 401
    res = await client.post("/api/me/progress/update",
                            params={"unit_id": content.unit_a, "lesson_id": content.a_muf})
    assert res.status_code == 401


async def test_progress_is_created_then_listed_for_its_owner_only(client, register, content):
    student, other = await register(), await register()
    res = await _update(client, student.headers, unit_id=content.unit_a,
                        lesson_id=content.a_muf, score=10, status="completed")
    assert res.status_code == 200
    mine = (await client.get("/api/me/progress", headers=student.headers)).json()
    assert mine == [{"unit_id": content.unit_a, "lesson_id": content.a_muf, "status": "completed",
                     "score": 10, "attempts": 1, "time_spent_sec": 0}]
    assert (await client.get("/api/me/progress", headers=other.headers)).json() == []


async def test_repeat_update_keeps_best_score_and_counts_attempts(client, register, content):
    student = await register()
    common = {"unit_id": content.unit_a, "lesson_id": content.a_muf, "status": "completed"}
    await _update(client, student.headers, score=15, time_spent_sec=30, **common)
    await _update(client, student.headers, score=5, time_spent_sec=20, **common)
    row = (await client.get("/api/me/progress", headers=student.headers)).json()[0]
    assert (row["score"], row["attempts"], row["time_spent_sec"]) == (15, 2, 50)


async def test_progress_for_unknown_lesson_is_404(client, register, content):
    student = await register()
    res = await _update(client, student.headers, unit_id=content.unit_a, lesson_id=99999)
    assert res.status_code == 404


async def test_progress_is_filed_under_the_lessons_own_unit(client, register, content):
    student = await register()
    await _update(client, student.headers, unit_id=content.unit_b, lesson_id=content.a_muf)
    row = (await client.get("/api/me/progress", headers=student.headers)).json()[0]
    assert row["unit_id"] == content.unit_a


async def test_progress_rejects_unknown_status_and_caps_score(client, register, content):
    student = await register()
    bad = await _update(client, student.headers, unit_id=content.unit_a,
                        lesson_id=content.a_muf, status="hacked")
    assert bad.status_code == 422
    # The lesson holds 15 points in total (10 + 5); a larger claim is capped.
    await _update(client, student.headers, unit_id=content.unit_a,
                  lesson_id=content.a_muf, score=99999, status="completed")
    row = (await client.get("/api/me/progress", headers=student.headers)).json()[0]
    assert row["score"] == 15


async def test_progress_rejects_negative_numbers(client, register, content):
    student = await register()
    for field in ("score", "time_spent_sec"):
        res = await _update(client, student.headers, unit_id=content.unit_a,
                            lesson_id=content.a_muf, **{field: -5})
        assert res.status_code == 422


async def test_a_session_over_several_lessons_is_recorded_per_lesson(client, register, content):
    """What the exercises page sends after a mixed session: one row per lesson."""
    student = await register()
    for lesson, score in ((content.a_muf, 15), (content.a_hiwar, 10), (content.a_nahw, 15)):
        await _update(client, student.headers, unit_id=content.unit_a, lesson_id=lesson,
                      score=score, status="completed")
    rows = {row["lesson_id"]: row for row in
            (await client.get("/api/me/progress", headers=student.headers)).json()}
    assert {lesson: row["score"] for lesson, row in rows.items()} == {
        content.a_muf: 15, content.a_hiwar: 10, content.a_nahw: 15}
    assert all(row["status"] == "completed" and row["unit_id"] == content.unit_a for row in rows.values())
