"""Checking a student's answer against the stored correct answer."""

import re
import unicodedata

_HARAKAT_FIRST, _HARAKAT_LAST = "\u064b", "\u065f"   # Arabic diacritics (tanwin … wavy hamza)
_TATWEEL = "\u0640"                                    # elongation stroke
_INITIAL_ALEF = re.compile(r"(?<!\w)[أإآٱ]")
# Punctuation never decides whether an answer is right («من أين أنت» = «من أين أنت؟»).
_PUNCTUATION = re.compile(r"[؟?!.,،;؛:«»\"'()\[\]\-–—…]")
_SPACES = re.compile(r"\s+")
# Turkish İ/I/ı are compared as i, and â/î/û as a/i/u: typing on a keyboard
# without them is not an error.
_TURKISH_I = str.maketrans({"İ": "i", "I": "i", "ı": "i", "\u0307": None,
                            "â": "a", "Â": "a", "î": "i", "Î": "i", "û": "u", "Û": "u"})
# A stored answer may list accepted alternatives: «Kırsal / Köy», «أجل / بلى».
ALTERNATIVES_SEPARATOR = "/"


def normalize_answer(text: str) -> str:
    """Ignore vocalisation, initial alef variants, punctuation and spacing.

    Students type without diacritics, while the stored answers are fully
    vocalised. The frontend applies the same rule when a guest practises
    without logging in (src/features/exercises/answers.js).
    """
    stripped = "".join(
        ch for ch in unicodedata.normalize("NFC", text or "").translate(_TURKISH_I)
        if not (_HARAKAT_FIRST <= ch <= _HARAKAT_LAST) and ch not in (_TATWEEL, "\u0670")
    )
    stripped = _SPACES.sub(" ", _PUNCTUATION.sub(" ", stripped)).strip()
    return _INITIAL_ALEF.sub("ا", stripped.lower())


def accepted_answers(expected: str) -> list[str]:
    """The whole stored answer and each alternative in it, normalised."""
    forms = [expected or ""] + (expected or "").split(ALTERNATIVES_SEPARATOR)
    return [form for form in dict.fromkeys(normalize_answer(f) for f in forms) if form]


def is_correct_answer(given: str, expected: str) -> bool:
    answer = normalize_answer(given)
    return bool(answer) and answer in accepted_answers(expected)
