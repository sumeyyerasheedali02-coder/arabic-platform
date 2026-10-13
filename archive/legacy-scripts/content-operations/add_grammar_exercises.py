import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from sqlalchemy import text, select
from database import AsyncSessionLocal, Unit, Lesson, Exercise
from grammar_exercises_data import GRAMMAR_EXERCISES


def fix_answer(ans):
    if ans == "صحيح":
        return "صَحِيح"
    if ans == "خطأ":
        return "خَطَأ"
    return ans


def build_options(ex):
    t = ex["type"]
    if t == "true_false":
        return ["صَحِيح", "خَطَأ"]
    if t == "multiple_choice":
        return ex.get("options")
    return None


async def add_grammar():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Unit).order_by(Unit.unit_number))
        units = result.scalars().all()
        unit_map = {u.unit_number: u for u in units}

        total_added = 0
        for unit_num, data in GRAMMAR_EXERCISES.items():
            unit = unit_map.get(unit_num)
            if not unit:
                continue

            res = await db.execute(
                select(Lesson).where(
                    Lesson.unit_id == unit.id,
                    Lesson.lesson_type == "nahw"
                )
            )
            lesson_nahw = res.scalar_one_or_none()
            if not lesson_nahw:
                continue

            await db.execute(
                text("DELETE FROM exercises WHERE lesson_id = :lid"),
                {"lid": lesson_nahw.id}
            )

            ex_num = 0
            for ex in data["grammar"]:
                ex_num += 1
                db.add(Exercise(
                    unit_id=unit.id, lesson_id=lesson_nahw.id,
                    exercise_number=ex_num, exercise_type=ex["type"],
                    question_ar=ex["q"], correct_answer=fix_answer(ex["answer"]),
                    options=build_options(ex), hint_ar=ex.get("hint"),
                    difficulty=2, points=10,
                ))
                total_added += 1

            for ex in data["final_test"]:
                ex_num += 1
                db.add(Exercise(
                    unit_id=unit.id, lesson_id=lesson_nahw.id,
                    exercise_number=ex_num, exercise_type=ex["type"],
                    question_ar=ex["q"], correct_answer=fix_answer(ex["answer"]),
                    options=build_options(ex), hint_ar=ex.get("hint"),
                    difficulty=3, points=15,
                ))
                total_added += 1

            await db.flush()
            print(f"وحدة {unit_num}: تم")

        await db.commit()
        print(f"تم اضافة {total_added} تمرينا بنجاح")


if __name__ == "__main__":
    asyncio.run(add_grammar())