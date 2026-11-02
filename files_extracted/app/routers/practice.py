"""Resumable practice sessions owned by the authenticated student."""
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import PracticeSession
from app.security import get_current_student
from app.services import practice

router = APIRouter(prefix="/api/me/practice", tags=["practice"])


class StartPractice(BaseModel):
    restart: bool = False
    mistakes_only: bool = False


class AdvancePractice(BaseModel):
    session_id: UUID
    index: int = Field(ge=0)


@router.get("/{unit_id}")
async def sessions(unit_id: int, student_id: int = Depends(get_current_student),
                   db: AsyncSession = Depends(get_db)):
    await practice.require_student(db, student_id)
    available = await practice.content(db, unit_id)
    rows = (await db.execute(select(PracticeSession).where(
        PracticeSession.student_id == student_id, PracticeSession.unit_id == unit_id,
    ))).scalars()
    return [practice.state(row, [ex for ex in available if practice.matches(ex, row.filter_key)])
            for row in rows]


@router.post("/{unit_id}/{key}")
async def start(unit_id: int, key: str, data: StartPractice,
                student_id: int = Depends(get_current_student), db: AsyncSession = Depends(get_db)):
    return await practice.start(db, student_id, unit_id, key,
                                restart=data.restart, mistakes_only=data.mistakes_only)


@router.post("/{unit_id}/{key}/advance")
async def advance(unit_id: int, key: str, data: AdvancePractice,
                  student_id: int = Depends(get_current_student), db: AsyncSession = Depends(get_db)):
    return await practice.advance(db, student_id, unit_id, key, str(data.session_id), data.index)
