"""Checking a student's answer against the stored correct answer."""

_HARAKAT_FIRST, _HARAKAT_LAST = "\u064b", "\u065f"   # Arabic diacritics (tanwin … wavy hamza)
_TATWEEL = "\u0640"                                    # elongation stroke


def normalize_answer(text: str) -> str:
    """Drop Arabic diacritics and tatweel, outer whitespace and letter case.

    Students type without diacritics, while the stored answers are fully
    vocalised. The frontend applies the same rule when a guest practises
    without logging in (src/features/exercises/answers.js).
    """
    stripped = "".join(
        ch for ch in text.strip()
        if not (_HARAKAT_FIRST <= ch <= _HARAKAT_LAST) and ch != _TATWEEL
    )
    return stripped.strip().lower()


def is_correct_answer(given: str, expected: str) -> bool:
    return normalize_answer(given) == normalize_answer(expected)
