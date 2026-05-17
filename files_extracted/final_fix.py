import os

m = open("main.py", encoding="utf-8").read()

old = '''@app.get("/api/units")
async def get_units(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Unit).order_by(Unit.unit_number))
    units = result.scalars().all()
    if not units:
        try:
            from seed_database import seed
            await seed()
            result = await db.execute(select(Unit).order_by(Unit.unit_number))
            units = result.scalars().all()
        except:
            pass
    if not units:
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from book1_part1_data import BOOK_1_PART_1
        return [{"id": i+1, "unit_number": u["number"], "title_ar": u["title_ar"], "title_tr": u["title_tr"], "description_ar": "", "description_tr": ""} for i, u in enumerate(BOOK_1_PART_1["units"])]
    return units'''

new = '''@app.get("/api/units")
async def get_units(db: AsyncSession = Depends(get_db)):
    from book1_part1_data import BOOK_1_PART_1
    result = await db.execute(select(Unit).order_by(Unit.unit_number))
    units = result.scalars().all()
    if units:
        return units
    return [{"id": i+1, "unit_number": u["number"], "title_ar": u["title_ar"], "title_tr": u["title_tr"], "description_ar": "", "description_tr": ""} for i, u in enumerate(BOOK_1_PART_1["units"])]'''

if old in m:
    m = m.replace(old, new)
    print("replaced OK")
else:
    print("NOT FOUND - writing direct replacement")
    m = m.replace(
        '@app.get("/api/units")',
        '@app.get("/api/units_old_disabled")'
    )
    m = m.replace(
        'if __name__ == "__main__":',
        '''@app.get("/api/units")
async def get_units(db: AsyncSession = Depends(get_db)):
    from book1_part1_data import BOOK_1_PART_1
    result = await db.execute(select(Unit).order_by(Unit.unit_number))
    units = result.scalars().all()
    if units:
        return units
    return [{"id": i+1, "unit_number": u["number"], "title_ar": u["title_ar"], "title_tr": u["title_tr"], "description_ar": "", "description_tr": ""} for i, u in enumerate(BOOK_1_PART_1["units"])]

if __name__ == "__main__":'''
    )

open("main.py", "w", encoding="utf-8").write(m)
print("Done!")
