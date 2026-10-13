import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Lesson, Exercise
from sqlalchemy import select

FILTERS = {
    "اختيار": ("exercise_type", "multiple_choice"),
    "فراغ": ("exercise_type", "fill_blank"),
    "صح/خطأ": ("exercise_type", "true_false"),
    "ترجمة": ("exercise_type", ["translate_ar_tr","translate_tr_ar"]),
    "وصل": ("exercise_type", "match"),
    "مترادف": ("hint_ar", "مترادف"),
    "متعاكس": ("hint_ar", "ضد / متعاكس"),
    "جمع": ("hint_ar", "جمع الكلمة"),
    "استيعاب": ("hint_ar", "استيعاب قرائي"),
}

async def run():
    async with AsyncSessionLocal() as db:
        units = (await db.execute(select(Unit).order_by(Unit.unit_number))).scalars().all()
        header = "وحدة|اختيار|فراغ|صح/خطأ|ترجمة|وصل|مترادف|متعاكس|جمع|استيعاب"
        print(header)
        print("-"*75)
        empties = {}
        for u in units:
            lessons = (await db.execute(select(Lesson.id).where(Lesson.unit_id==u.id))).scalars().all()
            exs = (await db.execute(select(Exercise).where(Exercise.lesson_id.in_(lessons)))).scalars().all()
            counts = {}
            for name, (field, val) in FILTERS.items():
                if isinstance(val, list):
                    counts[name] = sum(1 for e in exs if getattr(e, field) in val)
                elif field == "hint_ar":
                    counts[name] = sum(1 for e in exs if e.hint_ar == val)
                else:
                    counts[name] = sum(1 for e in exs if e.exercise_type == val)
                if counts[name] == 0:
                    empties.setdefault(name, []).append(u.unit_number)
            row = f"{u.unit_number:>4} | {counts['اختيار']:>4} | {counts['فراغ']:>3} | {counts['صح/خطأ']:>5} | {counts['ترجمة']:>4} | {counts['وصل']:>3} | {counts['مترادف']:>4} | {counts['متعاكس']:>5} | {counts['جمع']:>3} | {counts['استيعاب']:>5}"
            print(row)
        print("\n=== التصنيفات الفارغة ===")
        for name, units_list in empties.items():
            print(f"  {name}: فارغ في {len(units_list)} وحدة → {units_list[:10]}{'...' if len(units_list)>10 else ''}")

asyncio.run(run())