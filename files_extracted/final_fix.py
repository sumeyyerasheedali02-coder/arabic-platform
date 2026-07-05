import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Lesson, Exercise
from sqlalchemy import select, text

async def run():
    async with AsyncSessionLocal() as db:
        # 1. تأكيد القاعدة: عدّ الوحدات
        n = (await db.execute(select(Unit))).scalars().all()
        print(f"عدد الوحدات في هذه القاعدة: {len(n)}  (يجب 48 = Railway)")
        if len(n) != 48:
            print("!!! قاعدة خاطئة - أوقفي ولا تكملي")
            return

        # 2. انسخ التشكيل الصحيح من سؤال وحدة 1 العامل
        u1 = (await db.execute(select(Unit).where(Unit.unit_number==1))).scalar_one()
        l1 = (await db.execute(select(Lesson.id).where(Lesson.unit_id==u1.id))).scalars().all()
        ex1 = (await db.execute(select(Exercise).where(Exercise.lesson_id.in_(l1)))).scalars().all()
        sample = next((e.question_ar for e in ex1 if "رَتّ" in e.question_ar or "رَتِّ" in e.question_ar), None)
        print(f"نموذج وحدة 1: {repr(sample[:15]) if sample else 'لا يوجد'}")
        prefix = sample.split(":")[0] if sample else "رَتِّب الكلِمات"
        print(f"البادئة المستخدمة: {repr(prefix)}")

        ORDER = {
            9: [("القميص / أشتري / هذا","أشتري هذا القميص"),("الكتاب / بكم / هذا","بكم هذا الكتاب"),("جميل / الثوب / هذا","هذا الثوب جميل"),("القلم / أريد / هذا","أريد هذا القلم"),("السعر / غالٍ / هذا","هذا السعر غالٍ")],
        }
        # احذف القديم الخاطئ في وحدة 9
        u9 = (await db.execute(select(Unit).where(Unit.unit_number==9))).scalar_one()
        nahw9 = (await db.execute(select(Lesson).where(Lesson.unit_id==u9.id, Lesson.lesson_type=="nahw"))).scalar_one()
        old = (await db.execute(select(Exercise).where(Exercise.lesson_id==nahw9.id))).scalars().all()
        for e in old:
            if "الكلمات" in (e.question_ar or "") or "الكلِمات" in (e.question_ar or ""):
                await db.delete(e)
        await db.flush()

        num = 500
        for words, ans in ORDER[9]:
            num += 1
            db.add(Exercise(
                unit_id=u9.id, lesson_id=nahw9.id, exercise_number=num,
                exercise_type="fill_blank",
                question_ar=f"{prefix}: {words}",
                correct_answer=ans, options=None,
                hint_ar="رتب الكلمات", difficulty=3, points=15,
            ))
        await db.commit()
        print(f"\nتمت إضافة 5 أسئلة لوحدة 9 بالتشكيل: {repr(prefix)}")
        print("افتحي وحدة 9 الآن وحدّثي بقوة")

asyncio.run(run())