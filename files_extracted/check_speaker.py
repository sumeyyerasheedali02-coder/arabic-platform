import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, DialogueLine
from sqlalchemy import select, or_

async def check():
    async with AsyncSessionLocal() as db:
        # سطور فيها speaker فارغ أو NULL
        r = await db.execute(select(DialogueLine).where(
            or_(DialogueLine.speaker == None, DialogueLine.speaker == "")
        ))
        bad = r.scalars().all()
        print(f"عدد السطور الفارغة (speaker): {len(bad)}")
        for line in bad[:5]:
            print(f"  id={line.id}, dialogue_id={line.dialogue_id}, speaker='{line.speaker}', text='{line.text_ar[:30] if line.text_ar else None}'")
        
        # تحقق من text_ar و translation_tr أيضاً
        r2 = await db.execute(select(DialogueLine).where(DialogueLine.text_ar == None))
        bad2 = r2.scalars().all()
        print(f"عدد السطور بدون نص عربي: {len(bad2)}")

asyncio.run(check())