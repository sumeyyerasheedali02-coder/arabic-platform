"""A student's own lesson progress."""
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import StudentProgress
from app.schemas import ProgressOut
from app.security import get_current_student

router = APIRouter(prefix="/api/me/progress", tags=["progress"])


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
    unit_id:        int,
    lesson_id:      int,
    score:          int = 0,
    time_spent_sec: int = 0,
    status:         str = "in_progress",
    student_id:     int = Depends(get_current_student),
    db:             AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(StudentProgress).where(
            and_(
                StudentProgress.student_id == student_id,
                StudentProgress.lesson_id  == lesson_id,
            )
        )
    )
    progress = result.scalar_one_or_none()

    if progress:
        progress.score          = max(progress.score, score)   # best attempt counts
        progress.attempts      += 1
        progress.time_spent_sec += time_spent_sec
        progress.status         = status
        if status == "completed":
            progress.completed_at = datetime.utcnow()
    else:
        progress = StudentProgress(
            student_id=student_id,
            unit_id=unit_id,
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
