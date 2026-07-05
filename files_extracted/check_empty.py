import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Lesson, Exercise
from sqlalchemy import select, func

async def check():
    async with AsyncSessionLocal() as db:
        units = (await db.execute(select(Unit).order_by(Unit.unit_number))).scalars().all()
        print(f"{'وحدة':<6}{'العنوان':<35}{'hiwar':<10}{'mufradat':<12}{'nahw':<8}")
        print("="*75)
        empty = []
        for u in units:
            lessons = (await db.execute(select(Lesson).where(Lesson.unit_id==u.id))).scalars().all()
            counts = {}
            for L in lessons:
                cnt = (await db.execute(select(func.count(Exercise.id)).where(Exercise.lesson_id==L.id))).scalar()
                counts[L.lesson_type] = cnt
            h = counts.get('hiwar', 0)
            m = counts.get('mufradat', 0)
            n = counts.get('nahw', 0)
            mark = " ⚠️" if (h+m+n) < 30 else ""
            print(f"{u.unit_number:<6}{u.title_ar[:32]:<35}{h:<10}{m:<12}{n:<8}{mark}")
            if (h+m+n) < 30:
                empty.append(u.unit_number)
        print(f"\nالوحدات الضعيفة (أقل من 30 تمرين): {empty}")

asyncio.run(check())