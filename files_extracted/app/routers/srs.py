"""Spaced-repetition review cards (SM-2) for the logged-in student."""
from datetime import date, datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import SRSCard, Vocabulary
from app.schemas import SRSCardOut, SRSReview
from app.security import get_current_student
from app.services.srs import sm2

router = APIRouter(prefix="/api/me/srs", tags=["srs"])

DUE_CARDS_PER_SESSION = 20


@router.get("/due", response_model=List[SRSCardOut])
async def get_due_srs_cards(
    student_id: int = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    # next_review is an ISO date string, so string comparison orders correctly.
    today = date.today().isoformat()
    result = await db.execute(
        select(SRSCard, Vocabulary)
        .join(Vocabulary, SRSCard.vocabulary_id == Vocabulary.id)
        .where(
            and_(SRSCard.student_id == student_id, SRSCard.next_review <= today)
        )
        .limit(DUE_CARDS_PER_SESSION)
    )
    rows = result.all()
    return [
        SRSCardOut(
            vocabulary_id=row.SRSCard.vocabulary_id,
            word_ar=row.Vocabulary.word_ar,
            translation_tr=row.Vocabulary.translation_tr,
            example_ar=row.Vocabulary.example_ar,
            next_review=row.SRSCard.next_review,
            interval_days=row.SRSCard.interval_days,
        )
        for row in rows
    ]


@router.post("/review")
async def review_srs_card(
    data:       SRSReview,
    student_id: int = Depends(get_current_student),
    db:         AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SRSCard).where(
            and_(
                SRSCard.student_id    == student_id,
                SRSCard.vocabulary_id == data.vocabulary_id,
            )
        )
    )
    card = result.scalar_one_or_none()

    if not card:
        card = SRSCard(student_id=student_id, vocabulary_id=data.vocabulary_id)
        db.add(card)

    srs_result = sm2(
        quality=data.quality,
        repetitions=card.repetitions,
        ease_factor=card.ease_factor,
        interval_days=card.interval_days,
    )

    card.interval_days = srs_result.interval_days
    card.ease_factor   = srs_result.ease_factor
    card.repetitions   = srs_result.repetitions
    card.next_review   = srs_result.next_review
    card.last_reviewed = datetime.utcnow()

    await db.commit()
    return {"next_review": srs_result.next_review, "interval_days": srs_result.interval_days}


@router.post("/add-unit/{unit_id}")
async def add_unit_to_srs(
    unit_id:    int,
    student_id: int = Depends(get_current_student),
    db:         AsyncSession = Depends(get_db),
):
    """إضافة جميع مفردات وحدة إلى بطاقات SRS للطالب"""
    vocab_result = await db.execute(
        select(Vocabulary).where(Vocabulary.unit_id == unit_id)
    )
    vocabs = vocab_result.scalars().all()
    added = 0
    for v in vocabs:
        exists = await db.execute(
            select(SRSCard).where(
                and_(SRSCard.student_id == student_id, SRSCard.vocabulary_id == v.id)
            )
        )
        if not exists.scalar_one_or_none():
            db.add(SRSCard(
                student_id=student_id,
                vocabulary_id=v.id,
                next_review=date.today().isoformat(),
            ))
            added += 1
    await db.commit()
    return {"added": added, "message": f"تمت إضافة {added} بطاقة جديدة"}
