"""Durable practice: ownership, atomic answer checkpoints, retries and content changes."""
from sqlalchemy import func, select, text

from ._app import models


def route(content, key='multiple_choice'):
    return f'/api/me/practice/{content.unit_a}/{key}'


async def begin(client, student, content, **options):
    response = await client.post(route(content), headers=student.headers, json=options)
    assert response.status_code == 200, response.text
    return response.json()


async def answer(client, student, content, session, value='kitap'):
    return await client.post('/api/exercises/submit', headers=student.headers, json={
        'exercise_id': content.ex_choice, 'student_answer': value,
        'practice_session_id': session['session_id'], 'practice_filter': 'multiple_choice',
    })


async def test_requires_login_and_rejects_staff(client, teacher, content):
    assert (await client.get(f'/api/me/practice/{content.unit_a}')).status_code == 401
    staff = await teacher()
    assert (await client.get(f'/api/me/practice/{content.unit_a}', headers=staff.headers)).status_code == 403
    assert (await client.post(route(content), headers=staff.headers, json={})).status_code == 403


async def test_answer_feedback_and_cursor_survive_new_client_request(client, register, content):
    student = await register()
    session = await begin(client, student, content)
    assert session['exercise_ids'] == [content.ex_choice]
    assert (await answer(client, student, content, session)).status_code == 200
    restored = (await client.get(f'/api/me/practice/{content.unit_a}', headers=student.headers)).json()[0]
    assert restored['current_index'] == 0
    assert restored['results'][0]['student_answer'] == 'kitap'
    assert restored['results'][0]['is_correct'] is True
    assert (await begin(client, student, content))['session_id'] == session['session_id']


async def test_retry_answer_is_idempotent_and_final_advance_counts_once(client, register, content, db):
    student = await register()
    session = await begin(client, student, content)
    first = await answer(client, student, content, session)
    retry = await answer(client, student, content, session)
    assert first.json() == retry.json()
    assert (await db.execute(select(func.count(models.ExerciseAnswer.id)))).scalar() == 1
    payload = {'session_id': session['session_id'], 'index': 0}
    first = await client.post(route(content) + '/advance', headers=student.headers, json=payload)
    retry = await client.post(route(content) + '/advance', headers=student.headers, json=payload)
    assert first.status_code == retry.status_code == 200
    assert first.json()['completed'] is True
    assert retry.json()['current_index'] == 1
    row = (await db.execute(select(models.StudentProgress))).scalar_one()
    assert row.attempts == 1 and row.score == 10 and row.status == 'completed'


async def test_restart_retains_history_and_rejects_old_window(client, register, content, db):
    student = await register()
    old = await begin(client, student, content)
    await answer(client, student, content, old)
    new = await begin(client, student, content, restart=True)
    assert old['session_id'] != new['session_id']
    assert new['results'] == [] and new['current_index'] == 0
    assert (await answer(client, student, content, old)).status_code == 409
    assert (await db.execute(select(func.count(models.ExerciseAnswer.id)))).scalar() == 1


async def test_sessions_are_private_to_account(client, register, content):
    owner, other = await register(), await register()
    session = await begin(client, owner, content)
    assert (await client.get(f'/api/me/practice/{content.unit_a}', headers=other.headers)).json() == []
    assert (await answer(client, other, content, session)).status_code == 409
    assert (await client.post(route(content) + '/advance', headers=other.headers,
                             json={'session_id': session['session_id'], 'index': 0})).status_code == 409


async def test_cannot_skip_or_answer_different_question(client, register, content):
    student = await register()
    session = await begin(client, student, content)
    assert (await client.post(route(content) + '/advance', headers=student.headers,
                             json={'session_id': session['session_id'], 'index': 0})).status_code == 409
    response = await client.post('/api/exercises/submit', headers=student.headers, json={
        'exercise_id': content.ex_blank, 'student_answer': 'عليكم',
        'practice_session_id': session['session_id'], 'practice_filter': 'multiple_choice',
    })
    assert response.status_code == 409


async def test_content_update_requires_explicit_restart(client, register, content, db):
    student = await register()
    session = await begin(client, student, content)
    exercise = await db.get(models.Exercise, content.ex_choice)
    exercise.question_ar = 'سؤال جديد'
    await db.commit()
    restored = (await client.get(f'/api/me/practice/{content.unit_a}', headers=student.headers)).json()[0]
    assert restored['stale'] is True
    assert (await answer(client, student, content, session)).status_code == 409
    assert (await client.post(route(content), headers=student.headers, json={})).status_code == 409
    assert (await begin(client, student, content, restart=True))['stale'] is False


async def test_mistake_review_only_contains_wrong_answers(client, register, content):
    student = await register()
    session = await begin(client, student, content)
    await answer(client, student, content, session, value='wrong')
    await client.post(route(content) + '/advance', headers=student.headers,
                      json={'session_id': session['session_id'], 'index': 0})
    review = await begin(client, student, content, mistakes_only=True)
    assert review['exercise_ids'] == [content.ex_choice] and review['results'] == []
    assert review['session_id'] != session['session_id']


async def test_category_questions_not_mixed_with_generic_types(client, register, content):
    student = await register()
    generic = await begin(client, student, content)
    assert content.ex_synonym not in generic['exercise_ids']
    synonym = await client.post(route(content, 'synonym'), headers=student.headers, json={})
    assert synonym.json()['exercise_ids'] == [content.ex_synonym]
    assert (await client.post(route(content, 'all'), headers=student.headers, json={})).status_code == 422


async def test_upgrade_creates_only_missing_practice_table(tmp_path):
    from sqlalchemy.ext.asyncio import create_async_engine

    from app.migrations import apply_migrations

    from ._app import Base

    engine = create_async_engine(f'sqlite+aiosqlite:///{(tmp_path / "practice-upgrade.db").as_posix()}')
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await apply_migrations(conn)
            await conn.execute(text('DROP TABLE student_practice_sessions'))
            await conn.execute(text("DELETE FROM schema_migrations WHERE id='0011_student_practice_sessions'"))
            await conn.execute(text("INSERT INTO students (name,email,password_hash) VALUES ('Keep','keep@test.dev','hash')"))
            assert await apply_migrations(conn) == ['0011_student_practice_sessions']
            assert await apply_migrations(conn) == []
            assert (await conn.execute(text('SELECT password_hash FROM students'))).scalar() == 'hash'
    finally:
        await engine.dispose()

async def test_multi_question_resume_advances_to_exact_next_question(client, register, content, db):
    student = await register()
    second = models.Exercise(unit_id=content.unit_a, lesson_id=content.a_muf, exercise_number=99,
                             exercise_type='multiple_choice', question_ar='ثانٍ', correct_answer='ev',
                             options=['kitap', 'ev'], points=10)
    db.add(second)
    await db.commit()
    session = await begin(client, student, content)
    assert session['exercise_ids'] == [content.ex_choice, second.id]
    await answer(client, student, content, session)
    advanced = await client.post(route(content) + '/advance', headers=student.headers,
                                 json={'session_id': session['session_id'], 'index': 0})
    assert advanced.json()['current_index'] == 1 and not advanced.json()['completed']
    restored = (await client.get(f'/api/me/practice/{content.unit_a}', headers=student.headers)).json()[0]
    assert restored['current_index'] == 1 and len(restored['results']) == 1
    assert (await answer(client, student, content, session)).status_code == 409
    response = await client.post('/api/exercises/submit', headers=student.headers, json={
        'exercise_id': second.id, 'student_answer': 'ev',
        'practice_session_id': session['session_id'], 'practice_filter': 'multiple_choice',
    })
    assert response.status_code == 200 and response.json()['is_correct']


async def test_simultaneous_submit_retries_save_one_answer(client, register, content, db):
    import asyncio

    student = await register()
    session = await begin(client, student, content)
    responses = await asyncio.gather(answer(client, student, content, session),
                                     answer(client, student, content, session))
    assert [response.status_code for response in responses] == [200, 200]
    assert (await db.execute(select(func.count(models.ExerciseAnswer.id)))).scalar() == 1


async def test_hidden_exercises_and_empty_filters_are_not_started(client, register, content, db):
    student = await register()
    exercise = await db.get(models.Exercise, content.ex_choice)
    exercise.is_hidden = True
    await db.commit()
    assert (await client.post(route(content), headers=student.headers, json={})).status_code == 400
    assert (await client.post(route(content, 'match'), headers=student.headers, json={})).status_code == 400
