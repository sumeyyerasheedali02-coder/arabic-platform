"""Add the supplementary book vocabulary to the database named by DATABASE_URL.

    python -m tools.add_vocabulary            # dry run: report what would be added
    python -m tools.add_vocabulary --apply    # add the words

The words are in content/vocabulary_supplement. Existing databases receive
them automatically through migration 0010 when the server starts; run this
tool to add them to a database that was seeded afterwards (`tools.seed` does
not load them), or to retry if that migration logged a failure.

Insert-only and repeatable: no existing row (words, students, answers,
progress, review cards) is changed or deleted, and words the database already
has are skipped. The run is one transaction. The database is shown before
anything happens.
"""
import argparse
import asyncio
import sys

from app.database import engine
from app.services.vocabulary_supplement import add_supplementary_vocabulary


async def run(apply: bool, log=print) -> dict:
    async with engine.begin() as conn:
        result = await add_supplementary_vocabulary(conn, apply=apply)
        plan = result.plan
        for number in sorted(plan.additions):
            log(f"  unit {number:>2}: +{len(plan.additions[number])}")
        if plan.missing_units:
            log(f"  not in the database, skipped: units {plan.missing_units}")
        totals = dict(to_add=plan.count, already_in_unit=len(plan.already_in_unit),
                      in_other_unit=len(plan.in_other_unit), vocabulary_before=result.vocabulary_before,
                      vocabulary_after=result.vocabulary_after)
        log(f"{'Applied' if result.applied else 'Dry run, nothing was changed'}: {totals}")
        if result.applied:
            log(f"Highest vocabulary id before this run: {result.highest_id_before}")
    return totals


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m tools.add_vocabulary",
                                     description=__doc__.split("\n")[0])
    parser.add_argument("--apply", action="store_true", help="add the words (without it: dry run)")
    args = parser.parse_args(argv)

    print(f"Database: {engine.url.render_as_string(hide_password=True)}")

    async def go():
        return await run(args.apply)

    asyncio.run(go())
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
