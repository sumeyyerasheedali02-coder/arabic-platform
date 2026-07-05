import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Exercise
from sqlalchemy import select

FILTER_WORD = 'رَتِّب'  # ما يبحث عنه الفلتر

async def check():
    async with AsyncSessionLocal() as db:
        all_ex = (await db.execute(select(Exercise))).scalars().all()
        ours = [e for e in all_ex if "الكلمات" in (e.question_ar or "")]
        print(f"كلمة الفلتر: {repr(FILTER_WORD)}")
        if ours:
            q = ours[0].question_ar
            print(f"أول 6 محارف من سؤالنا: {repr(q[:6])}")
            print(f"هل يحتوي سؤالنا على كلمة الفلتر؟ {FILTER_WORD in q}")
        # عدّ كم سؤال يطابق الفلتر فعليا
        match = sum(1 for e in all_ex if FILTER_WORD in (e.question_ar or ""))
        print(f"\nعدد الأسئلة التي يلتقطها الفلتر: {match}")

asyncio.run(check())