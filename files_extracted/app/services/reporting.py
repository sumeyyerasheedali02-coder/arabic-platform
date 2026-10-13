"""Aggregated figures for the teacher dashboard.

Each report runs a fixed number of queries, whatever the number of students
or units: totals are computed by the database with GROUP BY and matched to
the rows in memory.
"""
from typing import List

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ExerciseAnswer, Lesson, Student, StudentProgress, Unit
from app.schemas import StudentSummary, UnitStats

COMPLETED = "completed"


async def student_summaries(db: AsyncSession) -> List[StudentSummary]:
    """Every account, newest first, with its points and completed lessons."""
    students = (await db.execute(
        select(Student).order_by(Student.created_at.desc())
    )).scalars().all()

    # إجمالي النقاط: مجموع نقاط كل الإجابات المسجّلة
    points = dict((await db.execute(
        select(ExerciseAnswer.student_id, func.sum(ExerciseAnswer.points_earned))
        .group_by(ExerciseAnswer.student_id)
    )).all())

    # عدد الدروس المكتملة
    lessons_done = dict((await db.execute(
        select(StudentProgress.student_id, func.count(StudentProgress.id))
        .where(StudentProgress.status == COMPLETED)
        .group_by(StudentProgress.student_id)
    )).all())

    return [
        StudentSummary(
            student_id=s.id,
            name=s.name,
            email=s.email,
            total_score=points.get(s.id) or 0,
            lessons_done=lessons_done.get(s.id) or 0,
            last_active=s.last_login,
        )
        for s in students
    ]


def completion_percent(completed_lessons: int, students: int, lessons_in_unit: int) -> float:
    """Share of the unit that the students have completed, 0–100.

    Every student can complete every lesson of the unit once, so the whole is
    students x lessons. (Dividing by the number of students alone gave up to
    300% for a unit of three lessons.)
    """
    possible = students * lessons_in_unit
    if possible <= 0:
        return 0.0
    return round(min(completed_lessons / possible, 1.0) * 100, 1)


async def unit_stats(db: AsyncSession) -> List[UnitStats]:
    """Per unit: average progress score and how much of it the class completed."""
    units = (await db.execute(select(Unit).order_by(Unit.unit_number))).scalars().all()
    total_students = (await db.execute(select(func.count(Student.id)))).scalar() or 1

    # متوسط النقاط وعدد الدروس المكتملة لكل وحدة
    progress = {
        unit_id: (average, completed)
        for unit_id, average, completed in (await db.execute(
            select(
                StudentProgress.unit_id,
                func.avg(StudentProgress.score),
                func.sum(case((StudentProgress.status == COMPLETED, 1), else_=0)),
            ).group_by(StudentProgress.unit_id)
        )).all()
    }
    lessons_per_unit = dict((await db.execute(
        select(Lesson.unit_id, func.count(Lesson.id)).group_by(Lesson.unit_id)
    )).all())

    stats = []
    for unit in units:
        average, completed = progress.get(unit.id, (None, 0))
        lessons_in_unit = lessons_per_unit.get(unit.id) or unit.total_lessons or 0
        stats.append(UnitStats(
            unit_number=unit.unit_number,
            title_ar=unit.title_ar,
            avg_score=round(average or 0.0, 1),
            completion_pct=completion_percent(completed or 0, total_students, lessons_in_unit),
        ))
    return stats
