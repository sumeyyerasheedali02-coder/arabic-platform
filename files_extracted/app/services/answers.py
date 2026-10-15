"""Checking a student's answer against the stored correct answer."""

import re
import unicodedata

_HARAKAT_FIRST, _HARAKAT_LAST = "\u064b", "\u065f"   # Arabic diacritics (tanwin … wavy hamza)
_TATWEEL = "\u0640"                                    # elongation stroke
_INITIAL_ALEF = re.compile(r"(?<!\w)[أإآٱ]")


def normalize_answer(text: str) -> str:
    """Ignore vocalisation and initial alef variants when comparing answers.

    Students type without diacritics, while the stored answers are fully
    vocalised. The frontend applies the same rule when a guest practises
    without logging in (src/features/exercises/answers.js).
    """
    stripped = "".join(
        ch for ch in unicodedata.normalize("NFC", text).strip()
        if not (_HARAKAT_FIRST <= ch <= _HARAKAT_LAST) and ch not in (_TATWEEL, "\u0670")
    )
    return _INITIAL_ALEF.sub("ا", stripped.strip().lower())


def is_correct_answer(given: str, expected: str) -> bool:
    return normalize_answer(given) == normalize_answer(expected)
