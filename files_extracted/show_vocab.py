import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Unit, Vocabulary
from sqlalchemy import select

async def show():
    async with AsyncSessionLocal() as db:
        for n in range(17, 49):
            u = (await db.execute(select(Unit).where(Unit.unit_number==n))).scalar_one()
            words = (await db.execute(select(Vocabulary).where(Vocabulary.unit_id==u.id))).scalars().all()
            print(f"\n===== وحدة {n}: {u.title_ar} =====")
            for w in words:
                print(f"  {w.word_ar}  ←→  {w.translation_tr}")

asyncio.run(show())