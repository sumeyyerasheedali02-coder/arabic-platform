"""Shared Arabic–Turkish vocabulary, served straight from the content module.

Reference data, the same for everyone and tied to no student, so it needs no
database table: the «مفردات مشتركة» page reads it here. Open to guests.
"""
from fastapi import APIRouter

from content.shared_words import CATEGORIES

router = APIRouter(prefix="/api", tags=["shared-words"])


@router.get("/shared-words")
async def get_shared_words():
    """Every category with its words; the client groups, filters and searches."""
    total = sum(len(category["words"]) for category in CATEGORIES)
    return {"total": total, "categories": CATEGORIES}
