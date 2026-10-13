"""Teacher reports: scoped in SQL, fixed query counts, distinct lesson completion."""
from datetime import datetime, timedelta

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Exercise, ExerciseAnswer, Lesson, Student, StudentProgress, Unit
from app.schemas import StudentSummary, UnitStats

COMPLETED = "completed"


def completion_percent(completed_lessons: int, students: int, lessons_in_unit: int) -> float:
    possible = students * lessons_in_unit
    if possible <= 0:
        return 0.0
    return round(min(completed_lessons / possible, 1.0) * 100, 1)


def student_scope(sections: list[str] | None):
    query = select(Student.id).where(Student.role == "student")
    if sections is not None:
        query = query.where(Student.class_section.in_(sections))
    return query


async def student_summaries(
    db: AsyncSession, sections: list[str] | None = None, student_id: int | None = None,
) -> list[StudentSummary]:
    scope = student_scope(sections)
    if student_id is not None:
        scope = scope.where(Student.id == student_id)
    lesson_total = select(func.count(Lesson.id)).scalar_subquery()
    students = (await db.execute(
        select(Student, lesson_total).where(Student.id.in_(scope))
        .order_by(Student.created_at.desc(), Student.id.desc())
    )).all()
    progress = {
        sid: (done, active)
        for sid, done, active in (await db.execute(select(
            StudentProgress.student_id,
            func.count(func.distinct(case(
                (StudentProgress.status == COMPLETED, StudentProgress.lesson_id), else_=None))),
            func.max(StudentProgress.updated_at),
        ).where(StudentProgress.student_id.in_(scope)).group_by(StudentProgress.student_id))).all()
    }
    answers = {
        sid: (total, correct, active)
        for sid, total, correct, active in (await db.execute(select(
            ExerciseAnswer.student_id, func.count(ExerciseAnswer.id),
            func.sum(case((ExerciseAnswer.is_correct, 1), else_=0)),
            func.max(ExerciseAnswer.answered_at),
        ).where(ExerciseAnswer.student_id.in_(scope)).group_by(ExerciseAnswer.student_id))).all()
    }
    # Repeated correct answers do not inflate points: best points per exercise.
    best = select(
        ExerciseAnswer.student_id, ExerciseAnswer.exercise_id,
        func.max(ExerciseAnswer.points_earned).label("points"),
    ).where(ExerciseAnswer.student_id.in_(scope)).group_by(
        ExerciseAnswer.student_id, ExerciseAnswer.exercise_id).subquery()
    points = dict((await db.execute(select(best.c.student_id, func.sum(best.c.points))
                                    .group_by(best.c.student_id))).all())
    result = []
    for student, total_lessons in students:
        done, progress_active = progress.get(student.id, (0, None))
        count, correct, answer_active = answers.get(student.id, (0, 0, None))
        activity = [t for t in (student.last_login, progress_active, answer_active) if t is not None]
        result.append(StudentSummary(
            student_id=student.id, name=student.name, email=student.email,
            student_number=student.student_number,
            class_section=student.class_section, total_score=points.get(student.id) or 0,
            lessons_done=done, completion_pct=completion_percent(done, 1, total_lessons),
            last_active=max(activity) if activity else None, answers_count=count,
            correct_answers=correct or 0,
            accuracy_pct=round((correct or 0) / count * 100, 1) if count else None,
        ))
    return result


async def unit_stats(db: AsyncSession, sections: list[str] | None = None) -> list[UnitStats]:
    scope = student_scope(sections)
    student_count = select(func.count()).select_from(scope.subquery()).scalar_subquery()
    units = (await db.execute(select(Unit, student_count).order_by(Unit.unit_number))).all()
    distinct_progress = select(
        StudentProgress.student_id, StudentProgress.lesson_id, StudentProgress.unit_id,
        func.max(StudentProgress.score).label("score"),
        func.max(case((StudentProgress.status == COMPLETED, 1), else_=0)).label("completed"),
    ).where(StudentProgress.student_id.in_(scope)).group_by(
        StudentProgress.student_id, StudentProgress.lesson_id, StudentProgress.unit_id).subquery()
    progress = {
        uid: (average, done)
        for uid, average, done in (await db.execute(select(
            distinct_progress.c.unit_id, func.avg(distinct_progress.c.score),
            func.sum(distinct_progress.c.completed),
        ).group_by(distinct_progress.c.unit_id))).all()
    }
    lessons = dict((await db.execute(select(Lesson.unit_id, func.count(Lesson.id))
                                    .group_by(Lesson.unit_id))).all())
    return [UnitStats(
        unit_number=unit.unit_number, title_ar=unit.title_ar,
        avg_score=round(progress.get(unit.id, (0, 0))[0] or 0, 1),
        completion_pct=completion_percent(
            progress.get(unit.id, (0, 0))[1] or 0, students_count, lessons.get(unit.id, 0)),
    ) for unit, students_count in units]


async def student_details(db: AsyncSession, student_id: int) -> dict:
    summary = (await student_summaries(db, student_id=student_id))[0]
    progress = select(
        StudentProgress.lesson_id, func.max(StudentProgress.score).label("score"),
        func.sum(StudentProgress.attempts).label("attempts"),
        func.sum(StudentProgress.time_spent_sec).label("time_spent_sec"),
        func.max(case((StudentProgress.status == COMPLETED, 1), else_=0)).label("completed"),
        func.max(StudentProgress.updated_at).label("updated_at"),
    ).where(StudentProgress.student_id == student_id).group_by(StudentProgress.lesson_id).subquery()
    rows = (await db.execute(select(
        Lesson.id, Lesson.title_ar, Unit.unit_number, Unit.title_ar.label("unit_title"),
        progress.c.score, progress.c.attempts, progress.c.time_spent_sec,
        progress.c.completed, progress.c.updated_at,
    ).join(Unit, Lesson.unit_id == Unit.id).outerjoin(progress, progress.c.lesson_id == Lesson.id)
      .order_by(Unit.unit_number, Lesson.lesson_number))).mappings().all()
    lessons = [dict(row, status="completed" if row["completed"] else
                    "in_progress" if row["attempts"] else "not_started") for row in rows]
    day = func.date(ExerciseAnswer.answered_at)
    history = (await db.execute(select(
        day.label("date"), func.count(ExerciseAnswer.id).label("answers"),
        func.sum(case((ExerciseAnswer.is_correct, 1), else_=0)).label("correct"),
    ).where(ExerciseAnswer.student_id == student_id,
            ExerciseAnswer.answered_at >= datetime.utcnow() - timedelta(days=30))
      .group_by(day).order_by(day))).mappings().all()
    errors = (await db.execute(select(
        Exercise.question_ar, Exercise.exercise_type, ExerciseAnswer.student_answer,
        Exercise.correct_answer, ExerciseAnswer.answered_at,
    ).join(Exercise, Exercise.id == ExerciseAnswer.exercise_id)
      .where(ExerciseAnswer.student_id == student_id, ExerciseAnswer.is_correct.is_(False))
      .order_by(ExerciseAnswer.answered_at.desc(), ExerciseAnswer.id.desc()).limit(10))).mappings().all()
    return {"student": summary, "lessons": lessons,
            "history": [dict(row) for row in history], "recent_errors": [dict(row) for row in errors]}
