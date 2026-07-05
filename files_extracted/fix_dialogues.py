import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

content = open("main.py", encoding="utf-8").read()

# النص القديم الكامل للدالة (مع التحميل الكسول الذي يسبب الخطأ)
old = '''async def get_dialogues(lesson_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Dialogue)
        .where(Dialogue.lesson_id == lesson_id)
        .order_by(Dialogue.dialogue_number)
    )
    dialogues = result.scalars().all()
    # تحميل السطور لكل حوار
    for d in dialogues:
        lines_result = await db.execute(
            select(DialogueLine)
            .where(DialogueLine.dialogue_id == d.id)
            .order_by(DialogueLine.line_order)
        )
        d.lines = lines_result.scalars().all()
    return dialogues'''

# النص الجديد: استخدام selectinload لتحميل السطور بشكل صحيح ضمن async
new = '''async def get_dialogues(lesson_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Dialogue)
        .where(Dialogue.lesson_id == lesson_id)
        .order_by(Dialogue.dialogue_number)
        .options(selectinload(Dialogue.lines))
    )
    dialogues = result.scalars().all()
    return dialogues'''

if old in content:
    content = content.replace(old, new)
    # التأكد من وجود استيراد selectinload
    if "selectinload" not in content.split("async def get_dialogues")[0]:
        content = content.replace(
            "from sqlalchemy import",
            "from sqlalchemy.orm import selectinload\nfrom sqlalchemy import",
            1
        )
    open("main.py", "w", encoding="utf-8").write(content)
    print("✅ تم تعديل الدالة بنجاح")
    print("   - استبدال التحميل الكسول بـ selectinload")
    print("   - إضافة الاستيراد إن لزم")
else:
    print("❌ لم يُعثر على الدالة بالنص المتوقع")
    print("   لم يتغير أي شيء — الملف آمن")