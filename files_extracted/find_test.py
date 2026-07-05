import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Lesson, Exercise
from sqlalchemy import select, func

async def check():
    async with AsyncSessionLocal() as db:
        u = (await db.execute(select(Unit).where(Unit.unit_number==1))).scalar_one()
        print(f"وحدة 1: id={u.id}")
        lessons = (await db.execute(select(Lesson).where(Lesson.unit_id==u.id))).scalars().all()
        for L in lessons:
            cnt = (await db.execute(select(func.count(Exercise.id)).where(Exercise.lesson_id==L.id))).scalar()
            print(f"  درس '{L.lesson_type}': id={L.id}, تمارين={cnt}")
        # أين السؤال التجريبي؟
        e = (await db.execute(select(Exercise).where(Exercise.exercise_type=="antonym"))).scalar_one()
        print(f"\nالسؤال التجريبي في lesson_id={e.lesson_id}")
        # هل هذا الدرس ينتمي لوحدة 1؟
        L = (await db.execute(select(Lesson).where(Lesson.id==e.lesson_id))).scalar_one_or_none()
        if L:
            print(f"  هذا الدرس type='{L.lesson_type}', unit_id={L.unit_id}")
        else:
            print(f"  ⚠️ الدرس {e.lesson_id} غير موجود أصلاً!")

asyncio.run(check())