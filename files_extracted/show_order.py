import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Exercise
from sqlalchemy import select, or_

async def show():
    async with AsyncSessionLocal() as db:
        r = await db.execute(select(Exercise).where(
            or_(Exercise.question_ar.contains("رَتِّب"), Exercise.question_ar.contains("رتب"))
        ).limit(5))
        print("=== نماذج ترتيب الكلمات الموجودة ===")
        for e in r.scalars().all():
            print(f"  السؤال: {e.question_ar}")
            print(f"  الإجابة: {e.correct_answer}")
            print(f"  النوع: {e.exercise_type}")
            print(f"  hint: {e.hint_ar}")
            print()

asyncio.run(show())