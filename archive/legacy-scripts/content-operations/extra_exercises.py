import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Lesson, Exercise
from sqlalchemy import select, text

EXTRA = {
    1: {
        "antonym": [("ما عكس: نعم؟", "لا"), ("ما عكس: هذا؟", "هذه"), ("ما عكس: أنت (للمذكر)؟", "أنا")],
        "synonym": [("مرادف: مرحبا (تحية)؟", "السلام عليكم")],
    },
    2: {
        "antonym": [("ما عكس: الأب؟", "الأم"), ("ما عكس: الأخ؟", "الأخت"), ("ما عكس: الجد؟", "الجدة"), ("ما عكس: الابن؟", "الابنة"), ("ما عكس: الزوج؟", "الزوجة")],
    },
    3: {
        "antonym": [("ما عكس: كبير؟", "صغير"), ("ما عكس: جميل؟", "قبيح")],
        "plural": [("ما جمع: غرفة؟", "غرف"), ("ما جمع: كرسي؟", "كراسي")],
    },
    4: {
        "antonym": [("ما عكس: مبكرا؟", "متأخرا"), ("ما عكس: الصباح؟", "المساء"), ("ما عكس: النهار؟", "الليل"), ("ما عكس: يستيقظ؟", "ينام")],
    },
    5: {
        "antonym": [("ما عكس: جوعان؟", "شبعان"), ("ما عكس: عطشان؟", "ريان")],
        "plural": [("ما جمع: طعام؟", "أطعمة")],
    },
    6: {
        "antonym": [("ما عكس: يذهب؟", "يرجع")],
        "plural": [("ما جمع: مسجد؟", "مساجد"), ("ما جمع: صلاة؟", "صلوات"), ("ما جمع: ركعة؟", "ركعات")],
    },
    7: {
        "antonym": [("ما عكس: قريب من؟", "بعيد عن"), ("ما عكس: الطالب؟", "الطالبة")],
        "plural": [("ما جمع: كتاب؟", "كتب"), ("ما جمع: درس؟", "دروس"), ("ما جمع: طالب؟", "طلاب")],
    },
    8: {
        "antonym": [("ما عكس: الطبيب؟", "الطبيبة"), ("ما عكس: المعلم؟", "المعلمة")],
        "plural": [("ما جمع: طبيب؟", "أطباء"), ("ما جمع: مهندس؟", "مهندسون"), ("ما جمع: ساعة؟", "ساعات")],
    },
}

HINTS = {"antonym": "ضد / متعاكس", "plural": "جمع الكلمة", "synonym": "مترادف"}

async def run():
    async with AsyncSessionLocal() as db:
        units = {u.unit_number: u for u in (await db.execute(select(Unit))).scalars().all()}
        total = 0
        for unit_num, types in EXTRA.items():
            u = units.get(unit_num)
            if not u:
                continue
            nahw = (await db.execute(select(Lesson).where(
                Lesson.unit_id == u.id, Lesson.lesson_type == "nahw"))).scalar_one_or_none()
            if not nahw:
                continue
            await db.execute(text(
                "DELETE FROM exercises WHERE lesson_id = :lid AND exercise_type IN ('antonym','plural','synonym')"
            ), {"lid": nahw.id})
            num = 900
            for ex_type, items in types.items():
                for q, ans in items:
                    num += 1
                    db.add(Exercise(
                        unit_id=u.id, lesson_id=nahw.id, exercise_number=num,
                        exercise_type=ex_type, question_ar=q, correct_answer=ans,
                        options=None, hint_ar=HINTS.get(ex_type, "اكتب"), difficulty=2, points=10,
                    ))
                    total += 1
            await db.flush()
            print(f"وحدة {unit_num}: تم")
        await db.commit()
        print(f"تم اضافة {total} سؤالا")

asyncio.run(run())