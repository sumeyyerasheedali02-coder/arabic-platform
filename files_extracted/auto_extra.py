import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Lesson, Vocabulary, Exercise
from sqlalchemy import select, text

# ── قاموس المتعاكسات المعروفة (عربي: ضده) ──
ANTONYMS = {
    "كبير": "صغير", "صغير": "كبير", "جميل": "قبيح", "قريب": "بعيد", "بعيد": "قريب",
    "حار": "بارد", "بارد": "حار", "حر": "برد", "برد": "حر", "دافئ": "بارد",
    "جوعان": "شبعان", "عطشان": "ريان", "مبكرا": "متأخرا", "متأخر": "مبكر",
    "الصباح": "المساء", "المساء": "الصباح", "النهار": "الليل", "الليل": "النهار",
    "يذهب": "يرجع", "الذهاب": "الإياب", "أبيض": "أسود", "أسود": "أبيض",
    "سهل": "صعب", "صعب": "سهل", "قديم": "جديد", "جديد": "قديم",
    "كثير": "قليل", "قليل": "كثير", "أول": "آخر", "طويل": "قصير", "قصير": "طويل",
    "فقير": "غني", "غني": "فقير", "مفيد": "ضار", "سعيد": "حزين",
    "الحياة": "الموت", "النجاح": "الفشل", "الحلال": "الحرام", "الخير": "الشر",
    "الحرب": "السلام", "العدل": "الظلم", "القوة": "الضعف", "الصدق": "الكذب",
}

# ── قاموس الجمع المعروف (مفرد: جمعه) ──
PLURALS = {
    "غرفة": "غرف", "كرسي": "كراسي", "مسجد": "مساجد", "صلاة": "صلوات",
    "كتاب": "كتب", "درس": "دروس", "طالب": "طلاب", "طبيب": "أطباء",
    "ساعة": "ساعات", "بيت": "بيوت", "مدينة": "مدن", "قميص": "قمصان",
    "ثوب": "أثواب", "صديق": "أصدقاء", "هواية": "هوايات", "رحلة": "رحلات",
    "مجلة": "مجلات", "صحيفة": "صحف", "مكتبة": "مكتبات", "بلد": "بلاد",
    "حيوان": "حيوانات", "مثل": "أمثال", "كلمة": "كلمات", "نتيجة": "نتائج",
    "مشكلة": "مشاكل", "سبب": "أسباب", "موعد": "مواعيد", "دواء": "أدوية",
    "عيد": "أعياد", "شهر": "شهور", "فقير": "فقراء", "شخص": "أشخاص",
    "حق": "حقوق", "معجزة": "معجزات", "طفل": "أطفال", "عقل": "عقول",
    "حديث": "أحاديث", "أمة": "أمم", "وصية": "وصايا", "مهنة": "مهن",
    "جائزة": "جوائز", "نجم": "نجوم", "قصة": "قصص", "حق ": "حقوق",
}

def clean(word):
    # إزالة التشكيل و"ال" التعريف للمطابقة
    word = word.strip()
    for ch in "ًٌٍَُِّْ":
        word = word.replace(ch, "")
    return word

async def run():
    async with AsyncSessionLocal() as db:
        units = (await db.execute(select(Unit).where(
            Unit.unit_number >= 9, Unit.unit_number <= 48
        ).order_by(Unit.unit_number))).scalars().all()

        total = 0
        for u in units:
            nahw = (await db.execute(select(Lesson).where(
                Lesson.unit_id == u.id, Lesson.lesson_type == "nahw"))).scalar_one_or_none()
            if not nahw:
                continue

            # حذف الأنواع الإضافية القديمة فقط (آمن لإعادة التشغيل)
            await db.execute(text(
                "DELETE FROM exercises WHERE lesson_id = :lid AND exercise_type IN ('antonym','plural')"
            ), {"lid": nahw.id})

            # جلب مفردات الوحدة
            vocab = (await db.execute(select(Vocabulary).where(
                Vocabulary.unit_id == u.id))).scalars().all()

            antonyms_added = []
            plurals_added = []

            for v in vocab:
                w = clean(v.word_ar)
                # إزالة "ال" للبحث
                w_no_al = w[2:] if w.startswith("ال") else w
                # متعاكسات
                if len(antonyms_added) < 5:
                    for key in (w, w_no_al):
                        if key in ANTONYMS:
                            antonyms_added.append((f"ما عكس: {key}؟", ANTONYMS[key]))
                            break
                # جمع
                if len(plurals_added) < 5:
                    for key in (w, w_no_al):
                        if key in PLURALS:
                            plurals_added.append((f"ما جمع: {key}؟", PLURALS[key]))
                            break

            num = 900
            for q, ans in antonyms_added:
                num += 1
                db.add(Exercise(
                    unit_id=u.id, lesson_id=nahw.id, exercise_number=num,
                    exercise_type="antonym", question_ar=q, correct_answer=ans,
                    options=None, hint_ar="ضد / متعاكس", difficulty=2, points=10,
                ))
                total += 1
            for q, ans in plurals_added:
                num += 1
                db.add(Exercise(
                    unit_id=u.id, lesson_id=nahw.id, exercise_number=num,
                    exercise_type="plural", question_ar=q, correct_answer=ans,
                    options=None, hint_ar="جمع الكلمة", difficulty=2, points=10,
                ))
                total += 1

            await db.flush()
            print(f"وحدة {u.unit_number}: {len(antonyms_added)} متعاكسات + {len(plurals_added)} جمع")

        await db.commit()
        print(f"\nتم اضافة {total} سؤالا اجماليا")

asyncio.run(run())