import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Exercise
from sqlalchemy import select

async def check():
    async with AsyncSessionLocal() as db:
        r = await db.execute(select(Exercise).where(Exercise.lesson_id==2235).limit(4))
        for e in r.scalars().all():
            print(f"النوع: {e.exercise_type}")
            print(f"  السؤال: {e.question_ar[:40]}")
            print(f"  الصحيح: '{e.correct_answer}'")
            print(f"  الخيارات: {e.options}")
            print("  ---")

asyncio.run(check())