import asyncio, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Exercise
from sqlalchemy import select

async def check():
    async with AsyncSessionLocal() as db:
        # تمرين مفردات يعمل (true_false)
        r = await db.execute(select(Exercise).where(Exercise.exercise_type=="true_false").limit(3))
        print("=== تمارين صح/خطأ موجودة ===")
        for e in r.scalars().all():
            print(f"  correct_answer = '{e.correct_answer}'  | options = {e.options}")

asyncio.run(check())