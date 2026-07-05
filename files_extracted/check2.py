import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, ExerciseAnswer, Exercise
from sqlalchemy import select, desc

async def check():
    async with AsyncSessionLocal() as db:
        r = await db.execute(select(ExerciseAnswer).order_by(desc(ExerciseAnswer.id)).limit(5))
        print("=== آخر 5 إجابات للطالب ===")
        for a in r.scalars().all():
            ex = await db.get(Exercise, a.exercise_id)
            print(f"  أجاب: '{a.student_answer}'")
            print(f"  الصحيح: '{ex.correct_answer}'")
            print(f"  النوع: {ex.exercise_type} | صحيحة؟ {a.is_correct}")
            print("  ---")

asyncio.run(check())