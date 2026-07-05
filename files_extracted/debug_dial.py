import asyncio, sys, traceback
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from database import AsyncSessionLocal, Dialogue, DialogueLine
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from schemas import DialogueOut

async def test():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Dialogue).where(Dialogue.lesson_id == 2233)
            .order_by(Dialogue.dialogue_number)
            .options(selectinload(Dialogue.lines))
        )
        dialogues = result.scalars().all()
        print(f"عدد الحوارات: {len(dialogues)}")
        try:
            for d in dialogues:
                out = DialogueOut.model_validate(d)
                print(f"  ✓ حوار {d.id}: {len(out.lines)} سطر — نجح التحويل")
            print("\n✅ كل الحوارات تعمل بنجاح!")
        except Exception:
            print("✗ فشل:")
            traceback.print_exc()

asyncio.run(test())