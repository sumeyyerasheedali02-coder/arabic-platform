"""Account-owned resumable practice. Answers, cursor and completion commit atomically."""
import hashlib
import json
from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select, update

from app.models import Exercise, ExerciseAnswer, PracticeSession, Student, StudentProgress, Unit
from app.services.answers import is_correct_answer

CATEGORY_FILTERS = {"synonym", "antonym", "plural", "comprehension", "word_order"}
TYPE_FILTERS = {
    "multiple_choice", "fill_blank", "true_false", "translate_ar_tr", "match", "form_sentence", "respond",
}


def matches(exercise, key):
    if key in CATEGORY_FILTERS:
        return exercise.category == key
    types = {"translate_ar_tr", "translate_tr_ar"} if key == "translate_ar_tr" else {key}
    return not exercise.category and exercise.exercise_type in types


def signature(exercises):
    fields = ("id", "lesson_id", "exercise_type", "category", "question_ar", "question_tr", "options",
              "correct_answer", "explanation_ar", "hint_ar", "hint_tr", "points")
    payload = [{name: getattr(ex, name) for name in fields} for ex in exercises]
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


async def require_student(db, student_id, *, lock=False):
    if lock and db.bind.dialect.name == "sqlite":
        await db.execute(update(Student).where(Student.id == student_id).values(id=Student.id))
    query = select(Student).where(Student.id == student_id)
    if lock:
        query = query.with_for_update()
    student = (await db.execute(query)).scalar_one()
    if student.role != "student":
        raise HTTPException(403, "التدريب المحفوظ مخصص للطلاب")


async def content(db, unit_id, key=None):
    if key is not None and key not in CATEGORY_FILTERS | TYPE_FILTERS:
        raise HTTPException(422, "نوع التدريب غير صالح")
    if await db.get(Unit, unit_id) is None:
        raise HTTPException(404, "الوحدة غير موجودة")
    exercises = list((await db.execute(select(Exercise).where(
        Exercise.unit_id == unit_id, Exercise.is_hidden.is_(False),
    ).order_by(Exercise.exercise_number, Exercise.id))).scalars())
    return [ex for ex in exercises if matches(ex, key)] if key else exercises


def state(session, available):
    return {
        "session_id": session.session_id, "filter_key": session.filter_key,
        "exercise_ids": session.exercise_ids, "results": session.results,
        "current_index": session.current_index, "completed": session.completed,
        "stale": session.content_signature != signature(available),
        "updated_at": session.updated_at.isoformat(),
    }


def ensure_current(session, session_id, available):
    if session is None or session.session_id != session_id:
        raise HTTPException(409, "تغيّرت الجلسة في نافذة أخرى؛ أعد فتح التدريب")
    if session.content_signature != signature(available):
        raise HTTPException(409, "تم تحديث محتوى التدريب؛ ابدأ جلسة جديدة")


async def start(db, student_id, unit_id, key, *, restart=False, mistakes_only=False):
    await require_student(db, student_id, lock=True)
    available = await content(db, unit_id, key)
    if not available:
        raise HTTPException(400, "لا توجد تمارين من هذا النوع في الوحدة")
    session = await db.get(PracticeSession, (student_id, unit_id, key))
    if session is not None and not restart and not mistakes_only:
        ensure_current(session, session.session_id, available)
        return state(session, available)
    ids = [ex.id for ex in available]
    if mistakes_only:
        if session is None or not session.completed:
            raise HTTPException(400, "أكمل التدريب أولًا لمراجعة الأخطاء")
        ensure_current(session, session.session_id, available)
        wrong = {r["exercise_id"] for r in session.results if not r["is_correct"]}
        ids = [ex_id for ex_id in ids if ex_id in wrong]
        if not ids:
            raise HTTPException(400, "لا توجد أخطاء لإعادتها")
    if session is None:
        session = PracticeSession(student_id=student_id, unit_id=unit_id, filter_key=key)
        db.add(session)
    session.session_id = str(uuid4())
    session.content_signature = signature(available)
    session.exercise_ids = ids
    session.results = []
    session.current_index = 0
    session.completed = False
    session.updated_at = datetime.utcnow()
    await db.commit()
    return state(session, available)


async def submit(db, student_id, data, exercise):
    await require_student(db, student_id, lock=True)
    available = await content(db, exercise.unit_id, data.practice_filter)
    session = await db.get(PracticeSession, (student_id, exercise.unit_id, data.practice_filter))
    ensure_current(session, data.practice_session_id, available)
    if session.completed or session.exercise_ids[session.current_index] != exercise.id:
        raise HTTPException(409, "هذا السؤال لا يطابق موضعك الحالي في التدريب")
    # A retry after a lost response returns the committed result, without a second answer.
    if len(session.results) > session.current_index:
        return session.results[session.current_index]
    correct = is_correct_answer(data.student_answer, exercise.correct_answer)
    result = {
        "exercise_id": exercise.id, "student_answer": data.student_answer,
        "is_correct": correct, "points_earned": exercise.points if correct else 0,
        "correct_answer": exercise.correct_answer, "explanation_ar": exercise.explanation_ar,
    }
    db.add(ExerciseAnswer(student_id=student_id, exercise_id=exercise.id,
                         student_answer=data.student_answer, is_correct=correct,
                         points_earned=result["points_earned"]))
    session.results = [*session.results, result]
    session.updated_at = datetime.utcnow()
    await db.commit()
    return result


async def record_completion(db, student_id, session, available):
    # Preserve the platform's existing lesson-completion rule, once per session.
    by_id = {ex.id: ex for ex in available}
    scores = {}
    for result in session.results:
        lesson_id = by_id[result["exercise_id"]].lesson_id
        if lesson_id is not None:
            scores[lesson_id] = scores.get(lesson_id, 0) + result["points_earned"]
    for lesson_id, score in scores.items():
        row = (await db.execute(select(StudentProgress).where(
            StudentProgress.student_id == student_id, StudentProgress.lesson_id == lesson_id,
        ).order_by(StudentProgress.id).limit(1))).scalar_one_or_none()
        if row is None:
            row = StudentProgress(student_id=student_id, unit_id=session.unit_id, lesson_id=lesson_id,
                                  score=score, attempts=1, time_spent_sec=0)
            db.add(row)
        else:
            row.score = max(row.score, score)
            row.attempts += 1
        row.status = "completed"
        row.completed_at = datetime.utcnow()


async def advance(db, student_id, unit_id, key, session_id, index):
    await require_student(db, student_id, lock=True)
    available = await content(db, unit_id, key)
    session = await db.get(PracticeSession, (student_id, unit_id, key))
    ensure_current(session, session_id, available)
    if index < session.current_index:
        return state(session, available)  # idempotent retry of an already acknowledged step
    if session.completed or index != session.current_index or len(session.results) <= index:
        raise HTTPException(409, "أجب عن السؤال الحالي قبل الانتقال")
    session.current_index += 1
    session.completed = session.current_index == len(session.exercise_ids)
    session.updated_at = datetime.utcnow()
    if session.completed:
        await record_completion(db, student_id, session, available)
    await db.commit()
    return state(session, available)
