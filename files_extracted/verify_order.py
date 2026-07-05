import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Lesson, Exercise
from sqlalchemy import select

FILTER_WORD = 'رَتِّب'

async def check():
    async with AsyncSessionLocal() as db:
        # افحص وحدة 9 تحديدا
        for unit_num in [1, 9]:
            u = (await db.execute(select(Unit).where(Unit.unit_number==unit_num))).scalar_one()
            lessons = (await db.execute(select(Lesson.id).where(Lesson.unit_id==u.id))).scalars().all()
            exs = (await db.execute(select(Exercise).where(Exercise.lesson_id.in_(lessons)))).scalars().all()
            order = [e for e in exs if FILTER_WORD in (e.question_ar or "")]
            print(f"وحدة {unit_num} (id={u.id}): {len(order)} سؤال ترتيب")
            for e in order[:2]:
                print(f"    {repr(e.question_ar[:30])}")
                print(f"    النوع: {e.exercise_type}")

asyncio.run(check())