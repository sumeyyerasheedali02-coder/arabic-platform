import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Dialogue, DialogueLine
from sqlalchemy import select

async def check():
    async with AsyncSessionLocal() as db:
        # حوارات الدرس 2233 (الذي يعطي خطأ 500)
        r = await db.execute(select(Dialogue).where(Dialogue.lesson_id == 2233))
        dials = r.scalars().all()
        print(f"عدد الحوارات في الدرس 2233: {len(dials)}")
        for d in dials:
            print(f"\nحوار id={d.id}, number={d.dialogue_number}, title={d.title_ar}")
            lines_r = await db.execute(select(DialogueLine).where(DialogueLine.dialogue_id == d.id))
            lines = lines_r.scalars().all()
            for L in lines:
                # تحقق من القيم الإشكالية
                issues = []
                if L.line_order is None: issues.append("line_order=NULL")
                if L.is_key_phrase is None: issues.append("is_key_phrase=NULL")
                if issues:
                    print(f"  سطر id={L.id}: {', '.join(issues)}")
            print(f"  (فحص {len(lines)} سطر)")

asyncio.run(check())