"""Teacher dashboard: every endpoint requires a teacher account."""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import StudentSummary, UnitStats
from app.security import get_current_teacher
from app.services import reporting

router = APIRouter(prefix="/api/teacher", tags=["teacher"])


@router.get("/students", response_model=List[StudentSummary])
async def get_all_students(
    teacher_id: int = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_db),
):
    return await reporting.student_summaries(db)


@router.get("/units/stats", response_model=List[UnitStats])
async def get_unit_stats(
    teacher_id: int = Depends(get_current_teacher),
    db: AsyncSession = Depends(get_db),
):
    return await reporting.unit_stats(db)
