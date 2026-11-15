"""Checking a student's answer against the stored correct answer."""

import re
import unicodedata

_HARAKAT_FIRST, _HARAKAT_LAST = "\u064b", "\u065f"   # Arabic diacritics (tanwin … wavy hamza)
_TATWEEL = "\u0640"                                    # elongation stroke
# Letters typed alike on a keyboard: «علىكم» for «عليكم», «مراة» for «مرآة». An alef
# with hamza inside a word is kept: سال ≠ سأل.
_LETTER_FOLD = str.maketrans({"آ": "ا", "ى": "ي"})
# The alef of a word, also after «ال» and its one-letter prefixes (وال، بال، كال، فال، لل):
# students type «الاخت» for «الأخت».
_INITIAL_ALEF = re.compile(r"(?<!\w)((?:[وفبكل]?ال|[وف]?لل)?)[أإٱ]")
# Typing «غرفه» for «غرفة» is not an error; inside a word the two letters stay distinct.
_FINAL_TA_MARBUTA = re.compile(r"ة(?!\w)")
# Punctuation never decides whether an answer is right («من أين أنت» = «من أين أنت؟»),
# and neither does the kind of apostrophe («Allah'a» = «Allah’a»).
_PUNCTUATION = re.compile(r"[؟?!.,،;؛:«»\"'’‘´`ʼ()\[\]\-–—…]")
_SPACES = re.compile(r"\s+")
# Turkish İ/I/ı are compared as i, and â/î/û as a/i/u: typing on a keyboard
# without them is not an error.
_TURKISH_I = str.maketrans({"İ": "i", "I": "i", "ı": "i", "\u0307": None,
                            "â": "a", "Â": "a", "î": "i", "Î": "i", "û": "u", "Û": "u"})
# A stored answer may list accepted alternatives: «Kırsal / Köy», «أجل / بلى».
ALTERNATIVES_SEPARATOR = "/"
# «مُهَنْدِسًا» is also written «مهندس»: the alef that carries a tanwin of fatha is optional.
_TANWIN_ALEF = re.compile(r"(?:\u064b\u0627|\u0627\u064b)(?=[\s.,،؟?!؛;:»\"')]|$)")


def normalize_answer(text: str) -> str:
    """Ignore vocalisation, alef/ya/ta marbuta spelling variants, punctuation and spacing.

    Students type without diacritics, while the stored answers are fully
    vocalised. The frontend applies the same rule when a guest practises
    without logging in (src/features/exercises/answers.js).
    """
    stripped = "".join(
        ch for ch in unicodedata.normalize("NFC", text or "").translate(_TURKISH_I)
        if not (_HARAKAT_FIRST <= ch <= _HARAKAT_LAST) and ch not in (_TATWEEL, "\u0670")
    )
    stripped = _SPACES.sub(" ", _PUNCTUATION.sub(" ", stripped)).strip()
    folded = _INITIAL_ALEF.sub(r"\1ا", stripped.lower().translate(_LETTER_FOLD))
    return _FINAL_TA_MARBUTA.sub("ه", folded)


def accepted_answers(expected: str) -> list[str]:
    """The whole stored answer and each alternative in it, normalised."""
    forms = [expected or ""] + (expected or "").split(ALTERNATIVES_SEPARATOR)
    return [form for form in dict.fromkeys(normalize_answer(f) for f in forms) if form]


CHOICE_TYPES = ("multiple_choice", "true_false", "match")


def is_typed_exercise(exercise_type: str | None, options) -> bool:
    """An exercise the student answers by typing (not by picking one of the options)."""
    return exercise_type not in CHOICE_TYPES and not options


def without_article(form: str) -> str:
    """A single normalised word without «ال»; phrases are left alone."""
    return form[2:] if " " not in form and form.startswith("ال") and len(form) > 3 else form


def _typed_keys(form: str) -> set[str]:
    """What a typed answer is compared by: without spaces («الحمدلله» = «الحمد لله»,
    «büyük anne» = «büyükanne») and, for a single word, with or without «ال»."""
    return {form.replace(" ", ""), without_article(form)}


def _tanwin_free_forms(expected: str) -> list[str]:
    forms = [expected or ""] + (expected or "").split(ALTERNATIVES_SEPARATOR)
    return [form for form in (_TANWIN_ALEF.sub("", f) for f in forms) if form not in forms]


def is_correct_answer(given: str, expected: str, typed: bool = False) -> bool:
    """`typed` exercises are compared more loosely: «قلم» for «القَلَم», «مهندس» for «مُهَنْدِسًا»,
    «الحمدلله» for «الحمد لله». Picking an option never is."""
    answer = normalize_answer(given)
    if not answer:
        return False
    accepted = accepted_answers(expected)
    if answer in accepted:
        return True
    if not typed:
        return False
    loose = set()
    for form in accepted + [normalize_answer(f) for f in _tanwin_free_forms(expected)]:
        loose |= _typed_keys(form)
    return bool(_typed_keys(answer) & loose)
