"""Add the supplementary vocabulary to a database that already has content.

`content/vocabulary_supplement` holds extra words for course units 1-32. This
module inserts the ones a database does not have yet. It is used by migration
`0010_supplementary_vocabulary` (existing databases get the words when the
server starts) and by `python -m tools.add_vocabulary`.

What it does, and nothing else:
- INSERTs rows into `vocabulary`. No row of any table is updated or deleted, so
  student accounts, answers, progress, review cards and the existing words
  (and their ids) are untouched. Review cards for the new words are not
  created here: a student gets one when they add the unit to their review or
  rate the word (see app/routers/srs.py).
- A word is skipped when the same word already exists, in the same unit or in
  any other unit, so nobody gets two cards for one word. Words are compared by
  letters (diacritics, alif forms and the definite article ignored); when both
  spellings carry diacritics they must agree too, so «رَأْي» (opinion) does not
  hide «رَأَى» (saw).
- A unit that is not in the database is skipped; running it twice adds nothing.
"""
import re
import unicodedata
from dataclasses import dataclass, field

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncConnection

from app.models import Lesson, Unit, Vocabulary
from content.vocabulary_supplement import SUPPLEMENT_VOCABULARY

SHADDA = "ّ"
SUKUN = "ْ"
# fathatan .. kasra and sukun, i.e. every mark that can end a word or carry a vowel
VOWEL_MARKS = "[ً-ْ]"
ALL_MARKS = "[ً-ٰٟـ]"  # + dagger alif, tatweel
ARTICLE = "^(?:وال|ال)"  # «وال» / «ال»


def letters_key(word: str) -> str:
    """The word's letters only: no diacritics, one alif, ى=ي, ة=ه, no leading «ال»."""
    word = re.sub(ALL_MARKS, "", word)
    word = re.sub("[أإآٱ]", "ا", word).replace("ى", "ي").replace("ة", "ه")
    word = re.sub(r"[؟?!،,.]", "", word).strip()
    return re.sub(ARTICLE + "(?=.{3})", "", word)


def vowel_key(word: str) -> str:
    """Like letters_key but keeping the diacritics, minus the ones that vary in print.

    Dropped: the marks on the last letter of each word (case endings), sukun,
    the short vowel before a long-vowel letter, and the marks on «ال» and on a
    hamzat-wasl alif.
    """
    word = unicodedata.normalize("NFC", word)
    word = word.replace("ٰ", "").replace("ـ", "").replace("ٱ", "ا")
    word = re.sub(f"([ً-ِ{SUKUN}]){SHADDA}", lambda match: SHADDA + match.group(1), word)
    word = word.replace(SUKUN, "")
    parts = []
    for token in re.split(r"[\s/،؟?]+", word):
        token = re.sub(f"[ً-{SHADDA}]+$", "", token)
        token = token.replace("َا", "ا")      # fatha + alif
        token = token.replace("ِي", "ي")      # kasra + ya
        token = token.replace("ُو", "و")      # damma + waw
        token = re.sub("[أإآٱ]", "ا", token).replace("ى", "ي").replace("ة", "ه")
        token = re.sub(f"{ARTICLE}{VOWEL_MARKS}*(?=.{{3}})", "", token)
        parts.append(re.sub(f"^ا{VOWEL_MARKS}*", "ا", token))
    return " ".join(parts)


def same_word(first: str, second: str) -> bool:
    if letters_key(first) != letters_key(second):
        return False
    both_vocalised = re.search(VOWEL_MARKS, first) and re.search(VOWEL_MARKS, second)
    return not both_vocalised or vowel_key(first) == vowel_key(second)


class WordIndex:
    """Words grouped by letters, so a comparison only looks at likely matches."""

    def __init__(self, words=()):
        self._by_letters: dict[str, list[str]] = {}
        for word in words:
            self.add(word)

    def add(self, word: str) -> None:
        self._by_letters.setdefault(letters_key(word), []).append(word)

    def has(self, word: str) -> bool:
        return any(same_word(word, other) for other in self._by_letters.get(letters_key(word), ()))

    def has_any_form(self, entry: str) -> bool:
        """A verb entry «ماضٍ / مضارع» counts as present when either form is."""
        forms = [part for part in re.split(r"\s*/\s*", entry) if part]
        return any(self.has(form) for form in [*forms, entry])


@dataclass
class SupplementPlan:
    """What would be added: `additions[unit_number] -> [word dicts]`."""
    additions: dict[int, list[dict]] = field(default_factory=dict)
    already_in_unit: list[tuple[int, str]] = field(default_factory=list)
    in_other_unit: list[tuple[int, str]] = field(default_factory=list)
    missing_units: list[int] = field(default_factory=list)

    @property
    def count(self) -> int:
        return sum(len(words) for words in self.additions.values())


def plan_additions(existing_by_unit: dict[int, list[str]], supplement=None) -> SupplementPlan:
    """Decide which supplement words a database with these words is missing.

    `existing_by_unit` maps unit number -> the words (word_ar) the unit has now.
    Pure: no database access.
    """
    supplement = SUPPLEMENT_VOCABULARY if supplement is None else supplement
    in_unit = {number: WordIndex(words) for number, words in existing_by_unit.items()}
    anywhere = WordIndex(word for words in existing_by_unit.values() for word in words)
    plan = SupplementPlan()
    for number, words in supplement.items():
        if number not in in_unit:
            plan.missing_units.append(number)
            continue
        for word in words:
            entry = word["word_ar"]
            if in_unit[number].has_any_form(entry):
                plan.already_in_unit.append((number, entry))
            elif anywhere.has_any_form(entry):
                plan.in_other_unit.append((number, entry))
            else:
                plan.additions.setdefault(number, []).append(word)
                in_unit[number].add(entry)
                anywhere.add(entry)
    return plan


@dataclass
class SupplementResult:
    plan: SupplementPlan
    applied: bool
    vocabulary_before: int
    vocabulary_after: int
    highest_id_before: int | None


async def add_supplementary_vocabulary(conn: AsyncConnection, *, apply: bool,
                                       supplement=None) -> SupplementResult:
    """Insert the missing words (or, with apply=False, only work out which).

    Runs on the caller's transaction; the caller commits. Only SELECTs and one
    INSERT into `vocabulary`.
    """
    unit_ids = {number: unit_id for unit_id, number in (await conn.execute(
        select(Unit.id, Unit.unit_number))).all()}
    number_of = {unit_id: number for number, unit_id in unit_ids.items()}

    words_by_unit: dict[int, list[str]] = {number: [] for number in unit_ids}
    lessons_used: dict[int, dict[int, int]] = {number: {} for number in unit_ids}
    for unit_id, lesson_id, word in (await conn.execute(
            select(Vocabulary.unit_id, Vocabulary.lesson_id, Vocabulary.word_ar))).all():
        number = number_of.get(unit_id)
        if number is None:
            continue
        words_by_unit[number].append(word)
        if lesson_id is not None:
            lessons_used[number][lesson_id] = lessons_used[number].get(lesson_id, 0) + 1

    vocabulary_lessons: dict[int, list[int]] = {}
    for lesson_id, unit_id in (await conn.execute(
            select(Lesson.id, Lesson.unit_id).where(Lesson.lesson_type == "mufradat")
            .order_by(Lesson.id))).all():
        vocabulary_lessons.setdefault(unit_id, []).append(lesson_id)

    plan = plan_additions(words_by_unit, supplement)
    before = (await conn.execute(select(func.count()).select_from(Vocabulary))).scalar()
    highest = (await conn.execute(select(func.max(Vocabulary.id)))).scalar()

    if apply and plan.count:
        rows = []
        for number, words in plan.additions.items():
            unit_id = unit_ids[number]
            lessons = vocabulary_lessons.get(unit_id, [])
            # The unit's vocabulary lesson; if it has several, the one its words already use.
            if len(lessons) == 1:
                lesson_id = lessons[0]
            elif lessons_used[number]:
                lesson_id = max(lessons_used[number], key=lessons_used[number].get)
            else:
                lesson_id = None
            rows.extend(dict(unit_id=unit_id, lesson_id=lesson_id, word_ar=word["word_ar"],
                             translation_tr=word["word_tr"], translation_en=word["word_en"],
                             difficulty=1) for word in words)
        await conn.execute(insert(Vocabulary.__table__), rows)

    after = (await conn.execute(select(func.count()).select_from(Vocabulary))).scalar()
    return SupplementResult(plan=plan, applied=apply and plan.count > 0, vocabulary_before=before,
                            vocabulary_after=after, highest_id_before=highest)
