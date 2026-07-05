import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Lesson, Dialogue, DialogueLine
from sqlalchemy import select, func

async def check():
    async with AsyncSessionLocal() as db:
        # افحص وحدة واحدة بالتفصيل الكامل
        for n in [1, 9, 25]:
            u = (await db.execute(select(Unit).where(Unit.unit_number==n))).scalar_one_or_none()
            if not u:
                continue
            print(f"\n===== وحدة {n}: {u.title_ar} (id={u.id}) =====")
            
            # كل الدروس
            lessons = (await db.execute(select(Lesson).where(Lesson.unit_id==u.id))).scalars().all()
            for L in lessons:
                print(f"  درس '{L.lesson_type}' (id={L.id})")
                # حوارات هذا الدرس
                dials = (await db.execute(select(Dialogue).where(Dialogue.lesson_id==L.id))).scalars().all()
                for d in dials:
                    lines = (await db.execute(select(func.count(DialogueLine.id)).where(DialogueLine.dialogue_id==d.id))).scalar()
                    print(f"    → حوار '{d.title_ar}' ({lines} سطر)")

asyncio.run(check())