import asyncio, sys, random
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Lesson, Vocabulary, Exercise
from sqlalchemy import select, text

async def run():
    async with AsyncSessionLocal() as db:
        units = (await db.execute(select(Unit).where(
            Unit.unit_number >= 9, Unit.unit_number <= 48
        ).order_by(Unit.unit_number))).scalars().all()

        total = 0
        for u in units:
            nahw = (await db.execute(select(Lesson).where(
                Lesson.unit_id==u.id, Lesson.lesson_type=="nahw"))).scalar_one_or_none()
            if not nahw:
                continue
            # حذف الوصل القديم فقط
            await db.execute(text(
                "DELETE FROM exercises WHERE lesson_id=:lid AND exercise_type='match'"
            ), {"lid": nahw.id})

            # جلب مفردات الوحدة
            vocab = (await db.execute(select(Vocabulary).where(
                Vocabulary.unit_id==u.id))).scalars().all()
            # تصفية المفردات ذات الترجمة الصالحة
            valid = [v for v in vocab if v.translation_tr and len(v.translation_tr) > 1]
            if len(valid) < 4:
                print(f"وحدة {u.unit_number}: مفردات غير كافية")
                continue

            # اختر 5 مفردات للأسئلة
            chosen = valid[:5]
            all_translations = [v.translation_tr for v in valid]

            num = 600
            for v in chosen:
                # 3 ترجمات خاطئة عشوائية + الصحيحة
                wrong = [t for t in all_translations if t != v.translation_tr]
                random.shuffle(wrong)
                opts = wrong[:3] + [v.translation_tr]
                random.shuffle(opts)
                num += 1
                db.add(Exercise(
                    unit_id=u.id, lesson_id=nahw.id, exercise_number=num,
                    exercise_type="match",
                    question_ar=f"صل: {v.word_ar}",
                    correct_answer=v.translation_tr,
                    options=opts, hint_ar=None, difficulty=2, points=10,
                ))
                total += 1
            await db.flush()
            print(f"وحدة {u.unit_number}: 5 وصل")
        await db.commit()
        print(f"\nتم اضافة {total} سؤال وصل")

asyncio.run(run())