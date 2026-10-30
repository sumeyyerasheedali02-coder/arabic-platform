"""Shared Arabic–Turkish vocabulary, served straight from the content module.

Reference data, the same for everyone and tied to no student, so it needs no
database table: the «مفردات مشتركة» page reads it here. Open to guests.
"""
from fastapi import APIRouter, HTTPException

from content.shared_words import CATEGORIES
from content.unit_shared_words import UNIT_SHARED_WORDS

router = APIRouter(prefix="/api", tags=["shared-words"])


@router.get("/shared-words")
async def get_shared_words():
    """Every category with its words; the client groups, filters and searches."""
    total = sum(len(category["words"]) for category in CATEGORIES)
    return {"total": total, "categories": CATEGORIES}


@router.get("/shared-words/units/{unit_number}")
async def get_unit_shared_words(unit_number: int):
    """The shared words that fit one unit's topic (by unit number, not database id)."""
    if unit_number not in UNIT_SHARED_WORDS:
        raise HTTPException(status_code=404, detail="لا توجد كلمات مشتركة لهذه الوحدة")
    words = UNIT_SHARED_WORDS[unit_number]
    return {"unit_number": unit_number, "total": len(words), "words": words}
