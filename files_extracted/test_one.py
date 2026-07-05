import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Lesson, Exercise
from sqlalchemy import select

async def add_test():
    async with AsyncSessionLocal() as db:
        u = (await db.execute(select(Unit).where(Unit.unit_number==1))).scalar_one()
        nahw = (await db.execute(select(Lesson).where(
            Lesson.unit_id==u.id, Lesson.lesson_type=="nahw"))).scalar_one()
        db.add(Exercise(
            unit_id=u.id, lesson_id=nahw.id, exercise_number=99,
            exercise_type="antonym",
            question_ar="[تجربة] ما عكس كلمة: كبير؟",
            correct_answer="صغير",
            options=None, hint_ar="اكتب الضد", difficulty=2, points=10,
        ))
        await db.commit()
        print("✅ أُضيف سؤال متعاكسات تجريبي لوحدة 1")
        print("   افتحي وحدة 1 → النحو → فلتر 'متعاكسات' → جرّبي حلّه")

asyncio.run(add_test())