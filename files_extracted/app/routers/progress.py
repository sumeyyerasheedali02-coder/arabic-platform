"""A student's own lesson progress."""
from datetime import datetime
from typing import List, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import (
    ActivityClock,
    ActivitySession,
    Exercise,
    ExerciseAnswer,
    Lesson,
    Student,
    StudentProgress,
)
from app.schemas import ProgressOut
from app.security import get_current_student

router = APIRouter(prefix="/api/me/progress", tags=["progress"])

ProgressStatus = Literal["not_started", "in_progress", "completed"]


class ActivityPing(BaseModel):
    session_id: UUID
    active_ms: int = Field(ge=0, le=2_000_000_000)
    lesson_id: int | None = Field(default=None, gt=0)


@router.post("/activity")
async def record_activity(
    ping: ActivityPing, student_id: int = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    # Serialize all of this student's tabs/devices. No progress scores,
    # completion flags or practice-attempt counters are changed by a timer.
    if db.bind.dialect.name == "sqlite":
        # SQLite ignores FOR UPDATE; acquire its writer lock before reading.
        await db.execute(update(Student).where(Student.id == student_id).values(id=Student.id))
    account = (await db.execute(select(Student).where(Student.id == student_id)
                               .with_for_update())).scalar_one()
    if account.role != "student":
        raise HTTPException(403, "تسجيل الوقت مخصص للطلاب")
    if ping.lesson_id is not None and await db.get(Lesson, ping.lesson_id) is None:
        raise HTTPException(404, "الدرس غير موجود")
    now = datetime.utcnow()
    clock = await db.get(ActivityClock, student_id)
    if clock is None:
        clock = ActivityClock(student_id=student_id, total_ms=0, updated_at=now)
        db.add(clock)
    session = await db.get(ActivitySession, (student_id, str(ping.session_id)))
    if session is None:
        session = ActivitySession(student_id=student_id, session_id=str(ping.session_id),
                                  lesson_id=ping.lesson_id, reported_ms=ping.active_ms,
                                  accepted_ms=0, updated_at=now)
        db.add(session)
    elif session.lesson_id != ping.lesson_id:
        raise HTTPException(409, "ابدأ جلسة جديدة عند تغيير الدرس")
    elif ping.active_ms > session.reported_ms:
        # Cumulative acknowledgements make retries/out-of-order requests harmless.
        # Server elapsed time also bounds concurrent tabs and fabricated durations.
        elapsed = max(0, int((now - clock.updated_at).total_seconds() * 1000))
        delta = min(ping.active_ms - session.reported_ms, elapsed, 60_000)
        session.reported_ms = ping.active_ms
        session.accepted_ms += delta
        if delta:
            session.updated_at = now
        clock.total_ms += delta
        clock.updated_at = now
    await db.commit()
    return {"recorded_ms": session.accepted_ms}


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
