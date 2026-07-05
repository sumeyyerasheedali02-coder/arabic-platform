import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Vocabulary, Exercise, Student, SRSCard
from sqlalchemy import select, func

async def check():
    async with AsyncSessionLocal() as db:
        units = (await db.execute(select(func.count(Unit.id)))).scalar()
        vocab = (await db.execute(select(func.count(Vocabulary.id)))).scalar()
        ex = (await db.execute(select(func.count(Exercise.id)))).scalar()
        students = (await db.execute(select(func.count(Student.id)))).scalar()
        srs = (await db.execute(select(func.count(SRSCard.id)))).scalar()
        # تمارين النحو تحديداً
        from database import Lesson
        nahw_ex = (await db.execute(
            select(func.count(Exercise.id)).join(Lesson, Exercise.lesson_id==Lesson.id)
            .where(Lesson.lesson_type=="nahw")
        )).scalar()
        print(f"الوحدات        : {units}")
        print(f"المفردات       : {vocab}")
        print(f"إجمالي التمارين: {ex}")
        print(f"تمارين النحو   : {nahw_ex}")
        print(f"الطلاب         : {students}")
        print(f"بطاقات SRS     : {srs}")

asyncio.run(check())