import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Lesson, Vocabulary, Exercise, Dialogue, DialogueLine, Student, SRSCard
from sqlalchemy import select, func

async def audit():
    async with AsyncSessionLocal() as db:
        units = (await db.execute(select(Unit).order_by(Unit.unit_number))).scalars().all()
        students_count = (await db.execute(select(func.count(Student.id)))).scalar()
        srs_count = (await db.execute(select(func.count(SRSCard.id)))).scalar()
        
        print("="*70)
        print("تقرير شامل للمنصة")
        print("="*70)
        print(f"عدد الطلاب المسجلين: {students_count}")
        print(f"عدد بطاقات SRS    : {srs_count}")
        print(f"عدد الوحدات        : {len(units)}")
        print()
        
        total_vocab = total_dial = total_lines = 0
        total_ex_h = total_ex_m = total_ex_n = 0
        weak_units = []
        
        for u in units:
            lessons = (await db.execute(select(Lesson).where(Lesson.unit_id==u.id))).scalars().all()
            vocab = (await db.execute(select(func.count(Vocabulary.id)).where(Vocabulary.unit_id==u.id))).scalar()
            dials = (await db.execute(select(Dialogue).join(Lesson).where(Lesson.unit_id==u.id))).scalars().all()
            lines_total = 0
            for d in dials:
                ln = (await db.execute(select(func.count(DialogueLine.id)).where(DialogueLine.dialogue_id==d.id))).scalar()
                lines_total += ln
            
            ex_h = ex_m = ex_n = 0
            for L in lessons:
                cnt = (await db.execute(select(func.count(Exercise.id)).where(Exercise.lesson_id==L.id))).scalar()
                if L.lesson_type == 'hiwar': ex_h = cnt
                elif L.lesson_type == 'mufradat': ex_m = cnt
                elif L.lesson_type == 'nahw': ex_n = cnt
            
            total_vocab += vocab
            total_dial += len(dials)
            total_lines += lines_total
            total_ex_h += ex_h
            total_ex_m += ex_m
            total_ex_n += ex_n
            
            total_ex = ex_h + ex_m + ex_n
            if ex_n == 0 or total_ex < 50:
                weak_units.append((u.unit_number, u.title_ar, vocab, ex_h, ex_m, ex_n))
        
        print(f"إجمالي المفردات         : {total_vocab}")
        print(f"إجمالي الحوارات         : {total_dial}")
        print(f"إجمالي سطور الحوارات    : {total_lines}")
        print(f"إجمالي تمارين الحوار    : {total_ex_h}")
        print(f"إجمالي تمارين المفردات  : {total_ex_m}")
        print(f"إجمالي تمارين النحو     : {total_ex_n}")
        print(f"المجموع الكلي للتمارين  : {total_ex_h + total_ex_m + total_ex_n}")
        print()
        print(f"الوحدات التي تحتاج تطوير ({len(weak_units)} وحدة):")
        print(f"{'رقم':<5}{'العنوان':<35}{'مفردات':<10}{'حوار':<8}{'مفردات':<10}{'نحو':<6}")
        print("-"*70)
        for w in weak_units:
            print(f"{w[0]:<5}{w[1][:32]:<35}{w[2]:<10}{w[3]:<8}{w[4]:<10}{w[5]:<6}")

asyncio.run(audit())