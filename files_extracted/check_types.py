import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Exercise
from sqlalchemy import select, func

async def check():
    async with AsyncSessionLocal() as db:
        r = await db.execute(
            select(Exercise.exercise_type, func.count(Exercise.id))
            .group_by(Exercise.exercise_type)
        )
        print("=== أنواع التمارين الموجودة وعددها ===")
        for t, c in r.all():
            print(f"  {t}: {c}")

asyncio.run(check())