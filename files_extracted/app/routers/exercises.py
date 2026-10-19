"""Exercises: listing (public) and answer submission (logged-in students)."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Exercise, ExerciseAnswer
from app.schemas import AnswerResult, AnswerSubmit, ExerciseOut
from app.security import get_current_student
from app.services.answers import is_correct_answer

router = APIRouter(prefix="/api", tags=["exercises"])


@router.get("/units/{unit_id}/exercises", response_model=List[ExerciseOut])
async def get_exercises(
    unit_id:    int,
    difficulty: Optional[int] = None,
    ex_type:    Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    # Hidden exercises were replaced or are surplus; their answers are kept.
    query = select(Exercise).where(Exercise.unit_id == unit_id, Exercise.is_hidden.is_(False))
    if difficulty:
        query = query.where(Exercise.difficulty == difficulty)
    if ex_type:
        query = query.where(Exercise.exercise_type == ex_type)
    # Numbers repeat between a unit's lessons; the id keeps the order stable.
    query = query.order_by(Exercise.exercise_number, Exercise.id)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/exercises/submit", response_model=AnswerResult)
async def submit_answer(
    data:       AnswerSubmit,
    student_id: int = Depends(get_current_student),
    db:         AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Exercise).where(Exercise.id == data.exercise_id))
    exercise = result.scalar_one_or_none()
    if not exercise:
        raise HTTPException(status_code=404, detail="التمرين غير موجود")

    is_correct = is_correct_answer(data.student_answer, exercise.correct_answer)
    points_earned = exercise.points if is_correct else 0

    # Every attempt is kept; the teacher report sums points_earned.
    db.add(ExerciseAnswer(
        student_id=student_id,
        exercise_id=data.exercise_id,
        student_answer=data.student_answer,
        is_correct=is_correct,
        points_earned=points_earned,
    ))
    await db.commit()

    return AnswerResult(
        is_correct=is_correct,
        correct_answer=exercise.correct_answer,
        explanation_ar=exercise.explanation_ar,
        points_earned=points_earned,
    )
