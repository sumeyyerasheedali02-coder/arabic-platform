"""Give every unit the same number of exercises of every kind.

    python -m tools.balance_exercises            # dry run: report what would change
    python -m tools.balance_exercises --apply    # make the change

Per unit, after the run: ten visible exercises of each kind (synonym, antonym,
plural, comprehension, fill-in, word order, translation, matching) from the
exercise bank (content/exercises/bank.py), and twenty multiple-choice and
twenty true/false questions (the existing ones that pass the checks, then
generated ones from the bank).

Nothing is deleted. Exercises that are replaced or beyond those numbers are
hidden (Exercise.is_hidden): students' answers on them, and the points they
earned, stay. Bank exercises already in the database are updated in place
when their text changes. One transaction; the dry run rolls it back.
"""
import argparse
import asyncio
import sys
from collections import Counter, defaultdict

from sqlalchemy import select

from app.database import AsyncSessionLocal, engine, init_db
from app.models import Exercise, Lesson, Unit, Vocabulary
from app.services.answers import accepted_answers, normalize_answer
from app.services.exercise_categories import exercise_category
from content.exercises.bank import (
    CHOICE_TARGET,
    FIRST_BANK_NUMBER,
    KINDS,
    REJECTED,
    VOCABULARY_RENAMES,
    full_bank,
)
from content.labels import ANSWER_FALSE

FIELDS = ("exercise_type", "question_ar", "correct_answer", "options", "hint_ar", "difficulty", "points")
MEANING_QUESTION = "مَا مَعْنَى كَلِمَة: "
EXTRA_NUMBERS = {KINDS["extra_choice"][0] // 100, KINDS["extra_true_false"][0] // 100}


def bucket(exercise) -> str:
    """The one filter of the exercises page an exercise belongs to."""
    category = exercise_category(exercise.exercise_type, exercise.hint_ar, exercise.question_ar)
    if category:
        return category
    return {"translate_tr_ar": "translate", "translate_ar_tr": "translate"}.get(
        exercise.exercise_type, exercise.exercise_type)


def is_bank(exercise) -> bool:
    return exercise.exercise_number >= FIRST_BANK_NUMBER


def unusable_choice(exercise, rejected: set, meanings: dict) -> bool:
    """An existing multiple-choice or true/false question that must not be shown.

    `meanings` maps each word of the unit to its accepted Turkish meanings.
    """
    if normalize_answer(exercise.question_ar) in rejected:
        return True
    right = set(accepted_answers(exercise.correct_answer))
    quoted = [part.split("»")[0] for part in exercise.question_ar.split("«")[1:]]
    if exercise.exercise_type == "multiple_choice":
        if exercise.question_ar.startswith(MEANING_QUESTION):
            # «ما معنى كلمة: X؟» built from an older, since corrected meaning of X.
            word = normalize_answer(exercise.question_ar[len(MEANING_QUESTION):])
            if word in meanings and not right & meanings[word]:
                return True
        options = [str(o) for o in exercise.options] if isinstance(exercise.options, list) else []
        matching = [o for o in options if normalize_answer(o) in right]
        overlapping = [o for o in options if set(accepted_answers(o)) & right]
        return len(matching) != 1 or len(overlapping) != 1
    if exercise.exercise_type == "true_false" and len(quoted) == 2:
        # «هل معنى «X» بالتركية: «Y»؟»: true only if Y is a meaning of X.
        word, shown = normalize_answer(quoted[0]), set(accepted_answers(quoted[1]))
        if word in meanings:
            says_true = normalize_answer(exercise.correct_answer) != normalize_answer(ANSWER_FALSE)
            return says_true != bool(shown & meanings[word])
    return False


async def balance(db, *, bank=None, log=print) -> dict:
    """Insert/update the bank and set every exercise's visibility. The caller commits."""
    from content.books import all_units

    bank = full_bank() if bank is None else bank
    vocabulary = {u["number"]: u["vocabulary"] for u in all_units()}
    # Words spelled alike without vowels (أَنْتَ / أَنْتِ) share one entry: either meaning counts.
    meanings = {number: defaultdict(set) for number in vocabulary}
    for number, words in vocabulary.items():
        for w in words:
            meanings[number][normalize_answer(w["word_ar"])] |= set(accepted_answers(w["word_tr"]))
    totals = Counter()
    units = {u.unit_number: u for u in (await db.execute(select(Unit))).scalars()}
    for number, rows in sorted(bank.items()):
        unit = units.get(number)
        if unit is None:
            continue
        # Vocabulary renames: fix the Arabic spelling in the database first,
        # so the meaning sync (which matches by exact word_ar) can find them.
        renames_for_unit = {old: new for (u, old), new in VOCABULARY_RENAMES.items() if u == number}
        if renames_for_unit:
            for word in (await db.execute(
                    select(Vocabulary).where(Vocabulary.unit_id == unit.id))).scalars():
                new_ar = renames_for_unit.get(word.word_ar)
                if new_ar and word.word_ar != new_ar:
                    word.word_ar = new_ar
                    totals["vocabulary_renamed"] += 1
            await db.flush()
        # Corrected meanings in content/books reach the vocabulary list (ids kept).
        # Matched by the exact vocalised spelling: يُحْضِر and يَحْضُر are different words.
        content_words = {w["word_ar"]: w for w in vocabulary[number]}
        for word in (await db.execute(select(Vocabulary).where(Vocabulary.unit_id == unit.id))).scalars():
            new = content_words.get(word.word_ar)
            if new and (word.translation_tr, word.translation_en) != (new["word_tr"], new["word_en"]):
                word.translation_tr, word.translation_en = new["word_tr"], new["word_en"]
                totals["vocabulary_corrected"] += 1
        lessons = {lesson.lesson_type: lesson.id for lesson in (await db.execute(
            select(Lesson).where(Lesson.unit_id == unit.id).order_by(Lesson.id))).scalars()}
        existing = {e.exercise_number: e for e in (await db.execute(select(Exercise).where(
            Exercise.unit_id == unit.id, Exercise.exercise_number >= FIRST_BANK_NUMBER))).scalars()}
        for row in rows:
            values = {k: row[k] for k in FIELDS}
            current = existing.get(row["exercise_number"])
            if current is None:
                db.add(Exercise(unit_id=unit.id, lesson_id=lessons[row["lesson"]],
                                exercise_number=row["exercise_number"], is_hidden=False, **values))
                totals["inserted"] += 1
            elif any(getattr(current, k) != v for k, v in values.items()):
                for k, v in values.items():
                    setattr(current, k, v)
                totals["updated"] += 1
        await db.flush()

        exercises = (await db.execute(select(Exercise).where(Exercise.unit_id == unit.id)
                                      .order_by(Exercise.exercise_number, Exercise.id))).scalars().all()
        rejected = {normalize_answer(q) for q in REJECTED.get(number, ())}
        by_bucket = defaultdict(list)
        for exercise in exercises:
            by_bucket[bucket(exercise)].append(exercise)
        visible = set()
        for name, members in by_bucket.items():
            if name in ("multiple_choice", "true_false"):
                own = [e for e in members
                       if not is_bank(e) and not unusable_choice(e, rejected, meanings[number])]
                extra = [e for e in members if is_bank(e)]
                visible |= {e.id for e in (own + extra)[:CHOICE_TARGET]}
            else:
                visible |= {e.id for e in members
                            if is_bank(e) and e.exercise_number // 100 not in EXTRA_NUMBERS}
        changed = 0
        for exercise in exercises:
            hidden = exercise.id not in visible
            if exercise.is_hidden != hidden:
                exercise.is_hidden = hidden
                changed += 1
        shown = Counter(bucket(e) for e in exercises if not e.is_hidden)
        totals["visibility_changed"] += changed
        totals["units"] += 1
        log(f"  unit {number:>2}: {dict(sorted(shown.items()))}")
    await db.flush()
    return dict(totals)


async def run(apply: bool, log=print) -> dict:
    async with AsyncSessionLocal() as db:
        totals = await balance(db, log=log)
        if apply:
            await db.commit()
        else:
            await db.rollback()
    log(f"{'Applied' if apply else 'Dry run, nothing was changed'}: {totals}")
    return totals


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m tools.balance_exercises",
                                     description=__doc__.split("\n")[0])
    parser.add_argument("--apply", action="store_true", help="make the change (without it: dry run)")
    args = parser.parse_args(argv)
    print(f"Database: {engine.url.render_as_string(hide_password=True)}")

    async def go():
        await init_db()
        await run(args.apply)

    asyncio.run(go())
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
