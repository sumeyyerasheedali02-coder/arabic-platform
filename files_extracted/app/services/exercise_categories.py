"""What an exercise practises, as a stable value the frontend can filter on.

`exercise_type` says how an exercise is answered (multiple choice, typed text,
…). Several kinds of content share one type, and the database tells them apart
only by the hint or the wording of the question. Deciding that in the browser
by comparing Arabic text exactly was fragile; it is decided here, once, on
text with the diacritics removed.
"""
from typing import Optional

from app.services.answers import normalize_answer
from content import labels

SYNONYM = "synonym"
ANTONYM = "antonym"
PLURAL = "plural"
COMPREHENSION = "comprehension"
WORD_ORDER = "word_order"

CATEGORIES = (SYNONYM, ANTONYM, PLURAL, COMPREHENSION, WORD_ORDER)

_BY_HINT = {
    normalize_answer(labels.HINT_SYNONYM): SYNONYM,
    normalize_answer(labels.HINT_ANTONYM): ANTONYM,
    normalize_answer(labels.HINT_PLURAL): PLURAL,
    normalize_answer(labels.HINT_COMPREHENSION): COMPREHENSION,
}
_WORD_ORDER_START = normalize_answer(labels.WORD_ORDER_VERB)          # "رتب"
_WORD_ORDER_HINT = normalize_answer(labels.HINT_WORD_ORDER)


def exercise_category(exercise_type: Optional[str], hint_ar: Optional[str],
                      question_ar: Optional[str]) -> Optional[str]:
    """Return one of CATEGORIES, or None for exercises that have no special category."""
    if exercise_type in (SYNONYM, ANTONYM, PLURAL, COMPREHENSION):
        return exercise_type
    hint = normalize_answer(hint_ar or "")
    if hint in _BY_HINT:
        return _BY_HINT[hint]
    if hint.startswith(_WORD_ORDER_HINT) or normalize_answer(question_ar or "").startswith(_WORD_ORDER_START):
        return WORD_ORDER
    return None
