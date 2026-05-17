m = open("main.py", encoding="utf-8").read()
old = """@app.get("/api/units")
async def get_units(db: AsyncSession = Depends(get_db)):
    from book1_part1_data import BOOK_1_PART_1
    result = await db.execute(select(Unit).order_by(Unit.unit_number))
    units = result.scalars().all()
    if units:
        return units
    return [{"id": i+1, "unit_number": u["number"], "title_ar": u["title_ar"], "title_tr": u["title_tr"], "description_ar": "", "description_tr": ""} for i, u in enumerate(BOOK_1_PART_1["units"])]"""
new = """@app.get("/api/units")
async def get_units(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Unit).order_by(Unit.unit_number))
    return result.scalars().all()"""
m = m.replace(old, new)
open("main.py", "w", encoding="utf-8").write(m)
print("Done!")
