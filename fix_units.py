import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform")
m = open(r"files_extracted\main.py", encoding="utf-8").read()
old = '''@app.get("/api/units", response_model=List[UnitOut])
async def get_units(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Unit).order_by(Unit.unit_number))
    return result.scalars().all()'''
new = '''@app.get("/api/units")
async def get_units(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Unit).order_by(Unit.unit_number))
    units = result.scalars().all()
    if not units:
        from seed_database import seed
        await seed()
        result = await db.execute(select(Unit).order_by(Unit.unit_number))
        units = result.scalars().all()
    return units'''
m = m.replace(old, new)
open(r"files_extracted\main.py", "w", encoding="utf-8").write(m)
print("Done!")
