"""Read-only learning content: units, lessons, vocabulary and dialogues (public)."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Dialogue, Lesson, Unit, Vocabulary
from app.schemas import DialogueOut, LessonOut, UnitOut, VocabularyOut

router = APIRouter(prefix="/api", tags=["content"])


# ── الوحدات ───────────────────────────────────────────────────
@router.get("/units")
async def get_units(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Unit).order_by(Unit.unit_number))
    return result.scalars().all()


@router.get("/units/{unit_id}", response_model=UnitOut)
async def get_unit(unit_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Unit).where(Unit.id == unit_id))
    unit = result.scalar_one_or_none()
    if not unit:
        raise HTTPException(status_code=404, detail="الوحدة غير موجودة")
    return unit


# ── الدروس ────────────────────────────────────────────────────
@router.get("/units/{unit_id}/lessons", response_model=List[LessonOut])
async def get_lessons(unit_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lesson)
        .where(Lesson.unit_id == unit_id)
        .order_by(Lesson.lesson_number)
    )
    return result.scalars().all()


@router.get("/lessons/{lesson_id}", response_model=LessonOut)
async def get_lesson(lesson_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="الدرس غير موجود")
    return lesson


# ── المفردات ──────────────────────────────────────────────────
@router.get("/units/{unit_id}/vocabulary", response_model=List[VocabularyOut])
async def get_vocabulary(unit_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Vocabulary)
        .where(Vocabulary.unit_id == unit_id)
        .order_by(Vocabulary.id)
    )
    return result.scalars().all()


@router.get("/vocabulary/search")
async def search_vocabulary(q: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Vocabulary).where(
            Vocabulary.word_ar.contains(q) | Vocabulary.translation_tr.contains(q)
        ).limit(20)
    )
    return result.scalars().all()


# ── الحوارات ──────────────────────────────────────────────────
@router.get("/lessons/{lesson_id}/dialogues", response_model=List[DialogueOut])
async def get_dialogues(lesson_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Dialogue)
        .where(Dialogue.lesson_id == lesson_id)
        .order_by(Dialogue.dialogue_number)
        # Lines must be loaded eagerly: lazy loading is not possible in async sessions.
        .options(selectinload(Dialogue.lines))
    )
    return result.scalars().all()
