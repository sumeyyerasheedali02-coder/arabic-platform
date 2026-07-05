import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Exercise
from sqlalchemy import select

async def show():
    async with AsyncSessionLocal() as db:
        # وصل
        r = await db.execute(select(Exercise).where(Exercise.exercise_type=="match").limit(3))
        print("=== نماذج وصل (match) ===")
        for e in r.scalars().all():
            print(f"  السؤال: {e.question_ar}")
            print(f"  الإجابة: {e.correct_answer}")
            print(f"  الخيارات: {e.options}")
            print(f"  hint: {e.hint_ar}")
            print()
        # ترتيب كلمات
        r2 = await db.execute(select(Exercise).where(Exercise.question_ar.contains("رَتِّب")).limit(3))
        print("=== نماذج ترتيب كلمات ===")
        for e in r2.scalars().all():
            print(f"  السؤال: {e.question_ar}")
            print(f"  الإجابة: {e.correct_answer}")
            print(f"  الخيارات: {e.options}")
            print(f"  hint: {e.hint_ar}")
            print()

asyncio.run(show())