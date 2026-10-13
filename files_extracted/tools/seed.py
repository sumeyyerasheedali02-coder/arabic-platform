"""Load the educational content into the database named by DATABASE_URL.

    python -m tools.seed
        Base content (48 units) into an EMPTY database. Does nothing if the
        database already has content.

    python -m tools.seed --with-supplements
        The same, followed by the supplementary exercise sets.

    python -m tools.seed --supplements-only [--yes-delete-affected-answers]
        Add (or rebuild) the supplementary sets on a database that already has
        the base content.

    python -m tools.seed --replace --yes-delete-student-activity [--with-supplements]
        Rebuild all content. This deletes every student's answers, lesson
        progress and review cards, because they point at content rows.

Student accounts are never deleted. Each run is a single transaction: if
anything fails, the database is left exactly as it was.
"""
import argparse
import asyncio
import random
import sys
from datetime import date

from sqlalchemy import delete, func, select, update

from app.database import AsyncSessionLocal, init_db
from app.models import (
    AISession, Dialogue, DialogueLine, Exercise, ExerciseAnswer, Lesson,
    SRSCard, Student, StudentProgress, Unit, Vocabulary,
)
from content import exercises as sets
from content.books import all_units

CONTENT_MODELS = (Unit, Lesson, Vocabulary, Dialogue, DialogueLine, Exercise)
# Deleted, in this order, when content is replaced.
ACTIVITY_MODELS = (SRSCard, ExerciseAnswer, StudentProgress)
CONTENT_DELETE_ORDER = (Exercise, DialogueLine, Dialogue, Vocabulary, Lesson, Unit)

# Supplementary sets live in the grammar lesson under reserved exercise numbers.
WORD_ORDER_BASE = 500
MATCH_BASE = 600
FILL_BLANK_BASE = 700
ENRICHMENT_BASE = 800
SUPPLEMENT_NUMBERS = (501, 999)
# "Match" and "translate" supplements are generated from the unit vocabulary
# for the units that have no hand-written base exercises.
GENERATED_FROM_UNIT = 9
GENERATED_PER_UNIT = 5

ENRICHMENT_HINTS = {
    "antonym": sets.HINT_ANTONYM,
    "plural": sets.HINT_PLURAL,
    "synonym": sets.HINT_SYNONYM,
    "comprehension": sets.HINT_COMPREHENSION,
}
TRUE_FALSE_OPTIONS = [sets.ANSWER_TRUE, sets.ANSWER_FALSE]


class ContentExistsError(RuntimeError):
    """Seeding would touch a database that already has content."""


class AnswersWouldBeDeletedError(RuntimeError):
    """Rebuilding exercises would delete recorded student answers."""


async def content_counts(db) -> dict:
    return {model.__tablename__: (await db.execute(select(func.count()).select_from(model))).scalar()
            for model in CONTENT_MODELS}


async def content_is_empty() -> bool:
    async with AsyncSessionLocal() as db:
        return not any((await content_counts(db)).values())


def _options(correct: str, pool: list[str], rng) -> list[str]:
    """The correct answer plus up to three other answers, shuffled."""
    others = [value for value in pool if value != correct]
    options = rng.sample(others, min(3, len(others))) + [correct]
    rng.shuffle(options)
    return options


# ── Base content ──────────────────────────────────────────────

def _vocabulary_exercises(vocab: list[dict], rng) -> list[dict]:
    """Two generated exercises per word: multiple choice and true/false."""
    translations = [word["word_tr"] for word in vocab]
    rows = []
    for index, word in enumerate(vocab):
        rows.append(dict(
            lesson="mufradat", exercise_type="multiple_choice",
            question_ar=f"مَا مَعْنَى كَلِمَة: {word['word_ar']}؟",
            correct_answer=word["word_tr"],
            options=_options(word["word_tr"], translations, rng),
            difficulty=1, points=10))

        # true/false alternates so that half of the statements are wrong
        others = [value for value in translations if value != word["word_tr"]]
        if index % 2 == 1 and others:
            shown, answer = rng.choice(others), sets.ANSWER_FALSE
        else:
            shown, answer = word["word_tr"], sets.ANSWER_TRUE
        rows.append(dict(
            lesson="mufradat", exercise_type="true_false",
            question_ar=f"هَلْ مَعْنَى «{word['word_ar']}» بِالتُّرْكِيَّة: «{shown}»؟",
            correct_answer=answer, options=list(TRUE_FALSE_OPTIONS),
            difficulty=1, points=5))
    return rows


def _handwritten_exercises(data: dict, rng) -> list[dict]:
    """Rows for one unit of content.exercises.EXERCISES_DATA."""
    rows = []
    for item in data.get("fill_blank", []):
        rows.append(dict(lesson="hiwar", exercise_type="fill_blank", question_ar=item["q"],
                         correct_answer=item["answer"], hint_ar=item.get("hint"),
                         options=None, difficulty=2, points=10))
    for item in data.get("translate_ar_tr", []):
        rows.append(dict(lesson="mufradat", exercise_type="translate_ar_tr",
                         question_ar=f"ترجم إلى التركية: {item['q']}",
                         correct_answer=item["answer"], options=item.get("options"),
                         difficulty=2, points=10))
    for item in data.get("translate_tr_ar", []):
        rows.append(dict(lesson="mufradat", exercise_type="translate_tr_ar",
                         question_ar=f"ترجم إلى العربية: {item['q']}",
                         correct_answer=item["answer"], options=item.get("options"),
                         difficulty=2, points=10))
    for group in data.get("match", []):
        answers = [pair["tr"] for pair in group["pairs"]]
        for pair in group["pairs"]:
            rows.append(dict(lesson="mufradat", exercise_type="match",
                             question_ar=f"صل: {pair['ar']}", correct_answer=pair["tr"],
                             options=_options(pair["tr"], answers, rng), difficulty=1, points=5))
    for kind, hint in (("synonyms", sets.HINT_SYNONYM), ("antonyms", sets.HINT_ANTONYM)):
        for item in data.get(kind, []):
            rows.append(dict(lesson="nahw", exercise_type="multiple_choice", question_ar=item["q"],
                             correct_answer=item["answer"], options=item.get("options"),
                             hint_ar=hint, difficulty=3, points=15))
    for item in data.get("word_order", []):
        rows.append(dict(lesson="hiwar", exercise_type="fill_blank",
                         question_ar=f"{sets.WORD_ORDER_PREFIX}: {' / '.join(item['words'])}",
                         correct_answer=item["answer"], hint_ar=item.get("hint"),
                         options=None, difficulty=3, points=15))
    for item in data.get("comprehension", []):
        rows.append(dict(lesson="hiwar", exercise_type="multiple_choice",
                         question_ar=item["passage"] + "\n\n" + item["q"],
                         correct_answer=item["answer"], options=item.get("options"),
                         hint_ar=sets.HINT_COMPREHENSION, difficulty=3, points=20))
    for item in data.get("plural", []):
        rows.append(dict(lesson="nahw", exercise_type="multiple_choice", question_ar=item["q"],
                         correct_answer=item["answer"], options=item.get("options"),
                         hint_ar=sets.HINT_PLURAL, difficulty=3, points=15))
    return rows


async def load_base_content(db, units=None, unit_exercises=None, rng=random, log=print) -> dict:
    """Insert units, lessons, dialogues, vocabulary and the base exercises.

    Every unit gets three lessons: dialogues (hiwar), vocabulary (mufradat)
    and grammar (nahw). The caller commits.
    """
    units = all_units() if units is None else units
    unit_exercises = sets.EXERCISES_DATA if unit_exercises is None else unit_exercises
    totals = dict(units=0, lessons=0, dialogues=0, vocabulary=0, exercises=0)

    for data in units:
        unit = Unit(
            unit_number=data["number"], title_ar=data["title_ar"], title_tr=data["title_tr"],
            description_ar=" | ".join(data["main_topics"]), description_tr=data["title_tr"],
            total_lessons=3)
        db.add(unit)
        await db.flush()

        lessons = {
            "hiwar": Lesson(unit_id=unit.id, lesson_number=1, title_ar="الحِوَارَات",
                            title_tr="Diyaloglar", lesson_type="hiwar"),
            "mufradat": Lesson(unit_id=unit.id, lesson_number=2, title_ar="المُفْرَدَات",
                               title_tr="Kelimeler", lesson_type="mufradat"),
            "nahw": Lesson(unit_id=unit.id, lesson_number=3, title_ar="النَّحْو وَالتَّرَاكِيب",
                           title_tr="Dilbilgisi", lesson_type="nahw",
                           grammar_focus=" | ".join(data["grammar"])),
        }
        db.add_all(lessons.values())
        await db.flush()

        for number, dialogue in enumerate(data["dialogues"], start=1):
            db.add(Dialogue(
                lesson_id=lessons["hiwar"].id, dialogue_number=number, title_ar=dialogue["title"],
                situation_tr="، ".join(dialogue["speakers"]),
                lines=[DialogueLine(line_order=order, speaker=line["speaker"], text_ar=line["text"],
                                    translation_tr=None, is_key_phrase=False)
                       for order, line in enumerate(dialogue["lines"], start=1)]))

        db.add_all(Vocabulary(
            unit_id=unit.id, lesson_id=lessons["mufradat"].id, word_ar=word["word_ar"],
            translation_tr=word["word_tr"], translation_en=word["word_en"], difficulty=1)
            for word in data["vocabulary"])

        rows = _vocabulary_exercises(data["vocabulary"], rng)
        rows += _handwritten_exercises(unit_exercises.get(data["number"], {}), rng)
        for number, row in enumerate(rows, start=1):
            lesson = lessons[row.pop("lesson")]
            db.add(Exercise(unit_id=unit.id, lesson_id=lesson.id, exercise_number=number, **row))
        await db.flush()

        totals["units"] += 1
        totals["lessons"] += 3
        totals["dialogues"] += len(data["dialogues"])
        totals["vocabulary"] += len(data["vocabulary"])
        totals["exercises"] += len(rows)
        log(f"  unit {unit.unit_number:>2}: {len(data['dialogues'])} dialogues, "
            f"{len(data['vocabulary'])} words, {len(rows)} exercises")
    return totals


# ── Supplementary exercise sets ───────────────────────────────

def _grammar_rows(data: dict) -> list[dict]:
    def row(item, difficulty, points):
        kind = item["type"]
        # The data spells the answers without diacritics; the buttons send them vocalised.
        answer = {"صحيح": sets.ANSWER_TRUE, "خطأ": sets.ANSWER_FALSE}.get(item["answer"], item["answer"])
        options = (list(TRUE_FALSE_OPTIONS) if kind == "true_false"
                   else item.get("options") if kind == "multiple_choice" else None)
        return dict(exercise_type=kind, question_ar=item["q"], correct_answer=answer,
                    options=options, hint_ar=item.get("hint"), difficulty=difficulty, points=points)

    return ([row(item, 2, 10) for item in data["grammar"]]
            + [row(item, 3, 15) for item in data["final_test"]])


class _ExerciseAdder:
    """Adds exercises to one lesson of one unit."""

    def __init__(self, db, unit_id: int, lesson_id: int):
        self.db, self.unit_id, self.lesson_id = db, unit_id, lesson_id

    def __call__(self, exercise_number: int, **fields) -> None:
        self.db.add(Exercise(unit_id=self.unit_id, lesson_id=self.lesson_id,
                             exercise_number=exercise_number, **fields))


async def apply_supplements(db, rng=random, log=print, allow_deleting_answers=False) -> dict:
    """Rebuild the supplementary sets in every unit's grammar lesson.

    Safe to repeat: the affected exercises are removed first. Where a unit has
    grammar questions, the whole grammar lesson is rebuilt (that is how those
    questions were introduced originally); elsewhere only exercise numbers
    501–999 are touched. Answers recorded for removed exercises are removed
    with them, which needs `allow_deleting_answers`. The caller commits.
    """
    totals = dict(grammar=0, word_order=0, match=0, fill_blank=0, translate=0, enrichment=0,
                  answers_deleted=0)
    units = (await db.execute(select(Unit).order_by(Unit.unit_number))).scalars().all()

    for unit in units:
        number = unit.unit_number
        nahw = (await db.execute(select(Lesson).where(
            Lesson.unit_id == unit.id, Lesson.lesson_type == "nahw").order_by(Lesson.id).limit(1)
        )).scalar_one_or_none()
        if nahw is None:
            continue

        stale = select(Exercise.id).where(Exercise.lesson_id == nahw.id)
        if number not in sets.GRAMMAR_EXERCISES:
            stale = stale.where(Exercise.exercise_number.between(*SUPPLEMENT_NUMBERS))
        stale_ids = list((await db.execute(stale)).scalars().all())
        if stale_ids:
            answers = (await db.execute(select(func.count()).select_from(ExerciseAnswer).where(
                ExerciseAnswer.exercise_id.in_(stale_ids)))).scalar()
            if answers and not allow_deleting_answers:
                raise AnswersWouldBeDeletedError(
                    f"unit {number}: {answers} recorded answer(s) belong to exercises that would "
                    "be rebuilt")
            await db.execute(delete(ExerciseAnswer).where(ExerciseAnswer.exercise_id.in_(stale_ids)))
            await db.execute(delete(Exercise).where(Exercise.id.in_(stale_ids)))
            totals["answers_deleted"] += answers

        add = _ExerciseAdder(db, unit.id, nahw.id)

        grammar = sets.GRAMMAR_EXERCISES.get(number)
        for index, row in enumerate(_grammar_rows(grammar) if grammar else [], start=1):
            add(index, **row)
            totals["grammar"] += 1

        for index, (words, answer) in enumerate(sets.WORD_ORDER.get(number, []), start=1):
            add(WORD_ORDER_BASE + index, exercise_type="fill_blank",
                question_ar=f"{sets.WORD_ORDER_PREFIX}: {words}", correct_answer=answer,
                options=None, hint_ar=sets.HINT_WORD_ORDER, difficulty=3, points=15)
            totals["word_order"] += 1

        vocabulary = []
        if number >= GENERATED_FROM_UNIT:
            vocabulary = (await db.execute(select(Vocabulary).where(
                Vocabulary.unit_id == unit.id).order_by(Vocabulary.id))).scalars().all()

        usable = [word for word in vocabulary if word.translation_tr and len(word.translation_tr) > 1]
        if len(usable) >= 4:
            translations = [word.translation_tr for word in usable]
            for index, word in enumerate(usable[:GENERATED_PER_UNIT], start=1):
                add(MATCH_BASE + index, exercise_type="match", question_ar=f"صل: {word.word_ar}",
                    correct_answer=word.translation_tr,
                    options=_options(word.translation_tr, translations, rng),
                    hint_ar=None, difficulty=2, points=10)
                totals["match"] += 1

        fill_number = FILL_BLANK_BASE
        for question, answer in sets.FILL_BLANK.get(number, []):
            fill_number += 1
            add(fill_number, exercise_type="fill_blank", question_ar=question,
                correct_answer=answer, options=None, hint_ar=sets.HINT_FILL_BLANK,
                difficulty=2, points=10)
            totals["fill_blank"] += 1
        for word in vocabulary[:GENERATED_PER_UNIT]:
            fill_number += 1
            add(fill_number, exercise_type="translate_ar_tr",
                question_ar=f"ترجم للتركية: {word.word_ar}", correct_answer=word.translation_tr,
                options=None, hint_ar=sets.HINT_TRANSLATE_TO_TURKISH, difficulty=2, points=10)
            totals["translate"] += 1

        enrichment_number = ENRICHMENT_BASE
        for kind, items in sets.ENRICHMENT.get(number, {}).items():
            for question, answer in items:
                enrichment_number += 1
                add(enrichment_number, exercise_type=kind, question_ar=question,
                    correct_answer=answer, options=None, hint_ar=ENRICHMENT_HINTS[kind],
                    difficulty=2, points=10)
                totals["enrichment"] += 1
        await db.flush()

    log(f"  supplements: {totals}")
    return totals


# ── Orchestration ─────────────────────────────────────────────

async def _delete_content_and_activity(db, log) -> None:
    await db.execute(update(AISession).values(unit_id=None))
    for model in ACTIVITY_MODELS + CONTENT_DELETE_ORDER:
        deleted = (await db.execute(delete(model))).rowcount
        log(f"  deleted {deleted} row(s) from {model.__tablename__}")


async def _cards_for_every_student(db, log) -> int:
    students = (await db.execute(select(Student.id))).scalars().all()
    words = (await db.execute(select(Vocabulary.id))).scalars().all()
    today = date.today().isoformat()
    db.add_all(SRSCard(student_id=student, vocabulary_id=word, ease_factor=2.5,
                       interval_days=1, repetitions=0, next_review=today)
               for student in students for word in words)
    log(f"  review cards: {len(students)} student(s) × {len(words)} word(s)")
    return len(students) * len(words)


async def seed(*, replace=False, with_supplements=False, srs_for_existing_students=False,
               units=None, unit_exercises=None, rng=random, log=print) -> dict:
    """Load the base content, optionally followed by the supplementary sets.

    Refuses to run on a database that already has content unless `replace` is
    set; `replace` also deletes all student activity (accounts are kept).
    """
    await init_db()
    async with AsyncSessionLocal() as db:
        counts = await content_counts(db)
        if any(counts.values()) and not replace:
            raise ContentExistsError(f"database already has content {counts}; nothing was changed")
        if replace:
            await _delete_content_and_activity(db, log)

        totals = await load_base_content(db, units=units, unit_exercises=unit_exercises,
                                         rng=rng, log=log)
        if with_supplements:
            totals["supplements"] = await apply_supplements(db, rng=rng, log=log)
        if srs_for_existing_students:
            totals["review_cards"] = await _cards_for_every_student(db, log)
        await db.commit()
    log(f"Done: {totals}")
    return totals


async def seed_if_empty(log=print) -> bool:
    """First-run bootstrap used at application start. Never deletes anything."""
    if not await content_is_empty():
        return False
    await seed(log=log)
    return True


async def supplements_only(*, allow_deleting_answers=False, rng=random, log=print) -> dict:
    await init_db()
    async with AsyncSessionLocal() as db:
        if not (await content_counts(db))["units"]:
            raise SystemExit("the database has no content yet; run `python -m tools.seed` first")
        totals = await apply_supplements(db, rng=rng, log=log,
                                         allow_deleting_answers=allow_deleting_answers)
        await db.commit()
    return totals


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m tools.seed",
        description="Load the educational content into the database named by DATABASE_URL.")
    parser.add_argument("--with-supplements", action="store_true",
                        help="also load the supplementary exercise sets")
    parser.add_argument("--supplements-only", action="store_true",
                        help="rebuild only the supplementary sets on existing content")
    parser.add_argument("--yes-delete-affected-answers", action="store_true",
                        help="with --supplements-only: allow deleting the answers recorded for "
                             "the exercises that are rebuilt")
    parser.add_argument("--replace", action="store_true",
                        help="delete existing content and ALL student answers, progress and "
                             "review cards, then load the content again")
    parser.add_argument("--yes-delete-student-activity", action="store_true",
                        help="required together with --replace")
    parser.add_argument("--srs-for-existing-students", action="store_true",
                        help="create a review card for every word for every existing student")
    args = parser.parse_args(argv)

    if args.replace and not args.yes_delete_student_activity:
        parser.error("--replace deletes every student's answers, progress and review cards; "
                     "add --yes-delete-student-activity to confirm")
    if args.supplements_only and (args.replace or args.with_supplements):
        parser.error("--supplements-only cannot be combined with --replace or --with-supplements")

    try:
        if args.supplements_only:
            asyncio.run(supplements_only(allow_deleting_answers=args.yes_delete_affected_answers))
        else:
            asyncio.run(seed(replace=args.replace, with_supplements=args.with_supplements,
                             srs_for_existing_students=args.srs_for_existing_students))
    except ContentExistsError as exc:
        print(f"Skipped: {exc}")
    except AnswersWouldBeDeletedError as exc:
        print(f"Stopped, nothing was changed: {exc}. "
              "Add --yes-delete-affected-answers to rebuild anyway.")
        return 1
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
