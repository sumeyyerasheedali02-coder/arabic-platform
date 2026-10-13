"""Read-only summary of the content in the database named by DATABASE_URL.

    python -m tools.content_report            # totals and anything that looks wrong
    python -m tools.content_report --units    # plus one line per unit

It only runs SELECT statements, so it is safe to point at production. Use it
to compare a database with what `python -m tools.seed [--with-supplements]`
produces (the expected numbers are printed at the end).
"""
import argparse
import asyncio
import sys
from collections import Counter, defaultdict

from sqlalchemy import func, select

from app.database import AsyncSessionLocal
from app.models import Dialogue, DialogueLine, Exercise, Lesson, Unit, Vocabulary
from content import exercises as sets
from tools.seed import SUPPLEMENT_NUMBERS

EXPECTED_BASE = dict(units=48, lessons=144, vocabulary=998, dialogues=140,
                     dialogue_lines=989, exercises=2129)
EXPECTED_WITH_SUPPLEMENTS = 4056

RANGES = (("base/grammar 1-499", 1, 499), ("word order 501-599", 501, 599),
          ("match 601-699", 601, 699), ("fill/translate 701-799", 701, 799),
          ("enrichment 801-899", 801, 899), ("superseded extras 901-999", 901, 999))


def _bucket(number: int) -> str:
    return next((name for name, low, high in RANGES if low <= number <= high), "other")


async def report(per_unit: bool) -> int:
    async with AsyncSessionLocal() as db:
        totals = {model.__tablename__: (await db.execute(
            select(func.count()).select_from(model))).scalar()
            for model in (Unit, Lesson, Vocabulary, Dialogue, DialogueLine, Exercise)}
        units = (await db.execute(select(Unit).order_by(Unit.unit_number))).scalars().all()
        lesson_type = dict((await db.execute(select(Lesson.id, Lesson.lesson_type))).all())
        rows = (await db.execute(select(
            Exercise.unit_id, Exercise.lesson_id, Exercise.exercise_number,
            Exercise.exercise_type, Exercise.question_ar))).all()

    by_type, by_range = Counter(), Counter()
    per_unit_types = defaultdict(Counter)
    problems = []
    unit_number = {unit.id: unit.unit_number for unit in units}
    for unit_id, lesson_id, number, kind, question in rows:
        by_type[kind] += 1
        in_grammar_lesson = lesson_type.get(lesson_id) == "nahw"
        bucket = _bucket(number) if in_grammar_lesson else "base/grammar 1-499"
        by_range[bucket] += 1
        per_unit_types[unit_id][lesson_type.get(lesson_id, "?")] += 1
        where = f"unit {unit_number.get(unit_id, '?')} exercise {number}"
        if "[تجربة]" in (question or ""):
            problems.append(f"{where}: leftover test question {question!r}")
        if in_grammar_lesson and SUPPLEMENT_NUMBERS[0] <= number <= 599 \
                and not (question or "").startswith(sets.WORD_ORDER_PREFIX):
            problems.append(f"{where}: word-order question does not start with the standard prefix")
        if bucket == "superseded extras 901-999":
            problems.append(f"{where}: belongs to an extra set that the enrichment set replaced")

    print("Rows:", totals)
    print("Exercises by type:", dict(by_type.most_common()))
    print("Exercises by number range:", dict(by_range))
    if per_unit:
        for unit in units:
            print(f"  unit {unit.unit_number:>2} {dict(per_unit_types[unit.id])}")
    numbers = [unit.unit_number for unit in units]
    if numbers != list(range(1, len(numbers) + 1)):
        problems.append(f"unit numbers are not 1..{len(numbers)}: {numbers}")

    print(f"\nExpected from tools.seed: {EXPECTED_BASE}")
    print(f"Expected exercises with supplements: {EXPECTED_WITH_SUPPLEMENTS}")
    if problems:
        print(f"\n{len(problems)} thing(s) to look at:")
        for line in problems[:40]:
            print("  -", line)
        if len(problems) > 40:
            print(f"  … and {len(problems) - 40} more")
    else:
        print("\nNothing unusual found.")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m tools.content_report",
                                     description=__doc__.split("\n")[0])
    parser.add_argument("--units", action="store_true", help="print one line per unit")
    args = parser.parse_args(argv)
    return asyncio.run(report(args.units))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
