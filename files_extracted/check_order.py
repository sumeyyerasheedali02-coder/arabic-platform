import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Exercise
from sqlalchemy import select

async def check():
    async with AsyncSessionLocal() as db:
        all_ex = (await db.execute(select(Exercise))).scalars().all()
        # ابحث عن "رَتِّب" بأي شكل
        order = [e for e in all_ex if "ر" in (e.question_ar or "") and "ت" in (e.question_ar or "") and "الكلمات" in (e.question_ar or "")]
        print(f"أسئلة فيها 'الكلمات': {len(order)}")
        for e in order[:3]:
            print(f"  {repr(e.question_ar[:25])}")
        # كل الأنواع
        from collections import Counter
        types = Counter(e.exercise_type for e in all_ex)
        print(f"\nإجمالي التمارين: {len(all_ex)}")
        print("الأنواع:", dict(types))

asyncio.run(check())