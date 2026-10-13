"""Aggregated figures for the teacher dashboard."""
from typing import List

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ExerciseAnswer, Student, StudentProgress, Unit
from app.schemas import StudentSummary, UnitStats


async def student_summaries(db: AsyncSession) -> List[StudentSummary]:
    result = await db.execute(select(Student).order_by(Student.created_at.desc()))
    students = result.scalars().all()

    summaries = []
    for s in students:
        # إجمالي النقاط
        score_result = await db.execute(
            select(func.sum(ExerciseAnswer.points_earned))
            .where(ExerciseAnswer.student_id == s.id)
        )
        total_score = score_result.scalar() or 0

        # عدد الدروس المكتملة
        lessons_result = await db.execute(
            select(func.count(StudentProgress.id))
            .where(
                and_(
                    StudentProgress.student_id == s.id,
                    StudentProgress.status == "completed",
                )
            )
        )
        lessons_done = lessons_result.scalar() or 0

        summaries.append(StudentSummary(
            student_id=s.id,
            name=s.name,
            email=s.email,
            total_score=total_score,
            lessons_done=lessons_done,
            last_active=s.last_login,
        ))

    return summaries


async def unit_stats(db: AsyncSession) -> List[UnitStats]:
    units_result = await db.execute(select(Unit).order_by(Unit.unit_number))
    units = units_result.scalars().all()
    stats = []

    for unit in units:
        # متوسط النقاط
        avg_result = await db.execute(
            select(func.avg(StudentProgress.score))
            .where(StudentProgress.unit_id == unit.id)
        )
        avg_score = avg_result.scalar() or 0.0

        # نسبة الإكمال
        total_students = await db.execute(select(func.count(Student.id)))
        total = total_students.scalar() or 1

        completed_result = await db.execute(
            select(func.count(StudentProgress.id)).where(
                and_(
                    StudentProgress.unit_id == unit.id,
                    StudentProgress.status  == "completed",
                )
            )
        )
        completed = completed_result.scalar() or 0

        stats.append(UnitStats(
            unit_number=unit.unit_number,
            title_ar=unit.title_ar,
            avg_score=round(avg_score, 1),
            completion_pct=round((completed / total) * 100, 1),
        ))

    return stats
