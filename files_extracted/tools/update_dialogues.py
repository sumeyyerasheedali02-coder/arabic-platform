"""Replace the dialogues of an existing database with those in content/books.

    python -m tools.update_dialogues            # dry run: report what would change
    python -m tools.update_dialogues --apply    # make the change

Only three things change, in each unit's first lesson (lesson_type "hiwar"):
its dialogues, their lines, and the lesson title (units 33-48 hold listening
texts). No student data refers to any of them: answers, progress, review cards
and active time point at units, lessons, exercises and words, which are kept
with their ids.

Works on the database named by DATABASE_URL, shown before anything happens.
The run is one transaction: the dry run executes the same statements and then
rolls back, and nothing is changed if any unit cannot be matched.
"""
import argparse
import asyncio
import sys

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from app.database import AsyncSessionLocal, engine, init_db
from app.models import Dialogue, DialogueLine, Lesson, Unit
from content.books import all_units
from tools.seed import dialogue_rows, hiwar_lesson_titles


class UnmatchedContentError(RuntimeError):
    """A unit of the content has no unit or no single dialogue lesson in the database."""


def _content_key(dialogues: list[dict]) -> list:
    return [(d["title"], [(line["speaker"], line["text"]) for line in d["lines"]]) for d in dialogues]


def _stored_key(dialogues: list[Dialogue]) -> list:
    return [(d.title_ar, [(line.speaker, line.text_ar) for line in d.lines]) for d in dialogues]


async def update_dialogues(*, apply: bool = False, units=None, log=print) -> dict:
    """Bring every unit's dialogues to the content; returns the totals.

    Raises UnmatchedContentError (and changes nothing) when a content unit has
    no unit, or not exactly one "hiwar" lesson, in the database.
    """
    units = all_units() if units is None else units
    totals = dict(units_changed=0, units_unchanged=0, dialogues_removed=0, dialogues_added=0,
                  lines_removed=0, lines_added=0, titles_changed=0)
    async with AsyncSessionLocal() as db:
        stored_units = {u.unit_number: u for u in (await db.execute(select(Unit))).scalars()}
        problems, plan = [], []
        for data in units:
            unit = stored_units.get(data["number"])
            if unit is None:
                problems.append(f"unit {data['number']}: not in the database")
                continue
            lessons = (await db.execute(select(Lesson).where(
                Lesson.unit_id == unit.id, Lesson.lesson_type == "hiwar"))).scalars().all()
            if len(lessons) != 1:
                problems.append(f"unit {data['number']}: {len(lessons)} dialogue lessons, expected 1")
                continue
            plan.append((data, lessons[0]))
        if problems:
            raise UnmatchedContentError("; ".join(problems))

        for data, lesson in plan:
            current = (await db.execute(
                select(Dialogue).where(Dialogue.lesson_id == lesson.id)
                .order_by(Dialogue.dialogue_number, Dialogue.id)
                .options(selectinload(Dialogue.lines)))).scalars().all()
            title_ar, title_tr = hiwar_lesson_titles(data["number"])
            same_text = _stored_key(current) == _content_key(data["dialogues"])
            same_title = (lesson.title_ar, lesson.title_tr) == (title_ar, title_tr)
            if same_text and same_title:
                totals["units_unchanged"] += 1
                continue

            totals["units_changed"] += 1
            if not same_title:
                lesson.title_ar, lesson.title_tr = title_ar, title_tr
                totals["titles_changed"] += 1
            if not same_text:
                old_lines = sum(len(d.lines) for d in current)
                new_lines = sum(len(d["lines"]) for d in data["dialogues"])
                ids = [d.id for d in current]
                if ids:
                    # Lines first: SQLite does not enforce the cascade, PostgreSQL would.
                    await db.execute(delete(DialogueLine).where(DialogueLine.dialogue_id.in_(ids)))
                    await db.execute(delete(Dialogue).where(Dialogue.id.in_(ids)))
                db.add_all(dialogue_rows(lesson.id, data["dialogues"]))
                totals["dialogues_removed"] += len(current)
                totals["dialogues_added"] += len(data["dialogues"])
                totals["lines_removed"] += old_lines
                totals["lines_added"] += new_lines
                log(f"  unit {data['number']:>2}: {len(current)} dialogue(s), {old_lines} line(s) -> "
                    f"{len(data['dialogues'])} dialogue(s), {new_lines} line(s)")
            if not same_title:
                log(f"  unit {data['number']:>2}: lesson title -> {title_tr}")
        await db.flush()

        if apply:
            await db.commit()
        else:
            await db.rollback()
    log(f"{'Applied' if apply else 'Dry run, nothing was changed'}: {totals}")
    return totals


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m tools.update_dialogues",
                                     description=__doc__.split("\n")[0])
    parser.add_argument("--apply", action="store_true",
                        help="make the change (without it: dry run)")
    args = parser.parse_args(argv)

    print(f"Database: {engine.url.render_as_string(hide_password=True)}")

    async def run():
        await init_db()
        return await update_dialogues(apply=args.apply)

    try:
        asyncio.run(run())
    except UnmatchedContentError as exc:
        print(f"Stopped, nothing was changed: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
