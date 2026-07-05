import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Lesson, Exercise
from sqlalchemy import select, func

async def check():
    async with AsyncSessionLocal() as db:
        u = (await db.execute(select(Unit).where(Unit.unit_number==1))).scalar_one()
        lessons = (await db.execute(select(Lesson).where(Lesson.unit_id==u.id))).scalars().all()
        print(f"=== دروس الوحدة 1 (id={u.id}) ===")
        for L in lessons:
            cnt = (await db.execute(select(func.count(Exercise.id)).where(Exercise.lesson_id==L.id))).scalar()
            print(f"  درس '{L.lesson_type}' (id={L.id}) → {cnt} تمرين")

asyncio.run(check())