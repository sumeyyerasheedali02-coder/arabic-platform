"""Spaced-repetition review cards (SM-2) for the logged-in student."""
from datetime import date, datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import SRSCard, Vocabulary
from app.schemas import SRSCardOut, SRSReview
from app.security import get_current_student
from app.services.srs import (
    NEW_CARD_EASE_FACTOR,
    NEW_CARD_INTERVAL_DAYS,
    NEW_CARD_REPETITIONS,
    preview_intervals,
    sm2,
)

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
            next_interval_days=preview_intervals(
                row.SRSCard.repetitions, row.SRSCard.ease_factor, row.SRSCard.interval_days),
        )
        for row in rows
    ]


@router.post("/review")
async def review_srs_card(
    data:       SRSReview,
    student_id: int = Depends(get_current_student),
    db:         AsyncSession = Depends(get_db),
):
    try:
        return await _apply_review(db, student_id, data)
    except IntegrityError:
        # A simultaneous request created this student's card for the word
        # first (one card per word is enforced); rate that card instead.
        await db.rollback()
        return await _apply_review(db, student_id, data)


async def _apply_review(db: AsyncSession, student_id: int, data: SRSReview) -> dict:
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
        # First review of a word that was never added to the student's cards.
        word = await db.execute(select(Vocabulary.id).where(Vocabulary.id == data.vocabulary_id))
        if word.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="الكلمة غير موجودة")
        # Set explicitly: column defaults are only applied when the row is
        # written, and SM-2 needs the numbers now.
        card = SRSCard(
            student_id=student_id, vocabulary_id=data.vocabulary_id,
            ease_factor=NEW_CARD_EASE_FACTOR, interval_days=NEW_CARD_INTERVAL_DAYS,
            repetitions=NEW_CARD_REPETITIONS,
        )
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
    words = (await db.execute(
        select(Vocabulary.id).where(Vocabulary.unit_id == unit_id).order_by(Vocabulary.id)
    )).scalars().all()
    # Words of this unit the student already has a card for (one query, not one per word)
    existing = set((await db.execute(
        select(SRSCard.vocabulary_id).where(
            SRSCard.student_id == student_id, SRSCard.vocabulary_id.in_(words))
    )).scalars().all()) if words else set()

    today = date.today().isoformat()
    new_cards = [
        {"student_id": student_id, "vocabulary_id": word, "next_review": today}
        for word in words if word not in existing
    ]
    added = 0
    if new_cards:
        # One multi-row INSERT; the remaining columns take their defaults. A
        # card a simultaneous request (double click) has just created is skipped.
        dialect = postgresql if db.bind.dialect.name == "postgresql" else sqlite
        inserted = await db.execute(dialect.insert(SRSCard).on_conflict_do_nothing(
            index_elements=["student_id", "vocabulary_id"]).returning(SRSCard.id), new_cards)
        added = len(inserted.all())
    await db.commit()
    return {"added": added, "message": f"تمت إضافة {added} بطاقة جديدة"}
