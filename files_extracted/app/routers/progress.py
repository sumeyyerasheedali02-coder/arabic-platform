"""A student's own lesson progress."""
from datetime import datetime
from typing import List, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Exercise, ExerciseAnswer, Lesson, StudentProgress
from app.schemas import ProgressOut
from app.security import get_current_student

router = APIRouter(prefix="/api/me/progress", tags=["progress"])

ProgressStatus = Literal["not_started", "in_progress", "completed"]


@router.get("/summary")
async def progress_summary(
    student_id: int = Depends(get_current_student), db: AsyncSession = Depends(get_db),
):
    best = select(func.max(ExerciseAnswer.points_earned).label("points")).where(
        ExerciseAnswer.student_id == student_id).group_by(ExerciseAnswer.exercise_id).subquery()
    total = (await db.execute(select(func.coalesce(func.sum(best.c.points), 0)))).scalar()
    return {"total_score": total}


@router.get("", response_model=List[ProgressOut])
async def get_my_progress(
    student_id: int = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(StudentProgress).where(StudentProgress.student_id == student_id)
    )
    return result.scalars().all()


@router.post("/update")
async def update_progress(
    lesson_id:      int,
    unit_id:        int = Query(0, description="ignored: the unit is taken from the lesson"),
    score:          int = Query(0, ge=0),
    time_spent_sec: int = Query(0, ge=0),
    status:         ProgressStatus = "in_progress",
    student_id:     int = Depends(get_current_student),
    db:             AsyncSession = Depends(get_db),
):
    """Record one practice session on a lesson.

    The score is reported by the client, so it is bounded here: it can never
    exceed the points the lesson's exercises are worth, and the row is always
    filed under the unit the lesson really belongs to.
    """
    lesson = (await db.execute(select(Lesson).where(Lesson.id == lesson_id))).scalar_one_or_none()
    if lesson is None:
        raise HTTPException(status_code=404, detail="الدرس غير موجود")

    lesson_points = (await db.execute(
        select(func.coalesce(func.sum(Exercise.points), 0)).where(Exercise.lesson_id == lesson_id)
    )).scalar()
    score = min(score, lesson_points)

    progress = (await db.execute(
        select(StudentProgress)
        .where(StudentProgress.student_id == student_id, StudentProgress.lesson_id == lesson_id)
        .order_by(StudentProgress.id)
        .limit(1)
    )).scalar_one_or_none()

    if progress:
        progress.unit_id        = lesson.unit_id
        progress.score          = max(progress.score, score)   # best attempt counts
        progress.attempts      += 1
        progress.time_spent_sec += time_spent_sec
        progress.status         = status
        if status == "completed":
            progress.completed_at = datetime.utcnow()
    else:
        progress = StudentProgress(
            student_id=student_id,
            unit_id=lesson.unit_id,
            lesson_id=lesson_id,
            score=score,
            attempts=1,
            time_spent_sec=time_spent_sec,
            status=status,
            completed_at=datetime.utcnow() if status == "completed" else None,
        )
        db.add(progress)

    await db.commit()
    return {"message": "تم تحديث التقدم"}
