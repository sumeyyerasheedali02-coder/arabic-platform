import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform")
m = open(r"files_extracted\main.py", encoding="utf-8").read()
m = m.replace('from database import (\n    get_db, init_db,', 'from database import (\n    get_db, init_db, AsyncSessionLocal,')
old_startup = '''@app.on_event("startup")
async def startup():
    await init_db()
    try:
        from seed_database import seed
        await seed()
        print("Seed completed successfully")
    except Exception as e:
        print(f"Seed error: {e}")
    async for db in get_db():
        result = await db.execute(select(Unit))
        unit = result.scalars().first()
        if not unit:
            from seed_database import seed
            await seed()
        break'''
new_startup = '''@app.on_event("startup")
async def startup():
    await init_db()
    try:
        from sqlalchemy import text
        async with AsyncSessionLocal() as db:
            result = await db.execute(text("SELECT COUNT(*) FROM units"))
            count = result.scalar()
        if count == 0:
            print("Database empty, running seed...")
            from seed_database import seed
            await seed()
            print("Seed done!")
        else:
            print(f"DB OK: {count} units")
    except Exception as e:
        print(f"Seed error: {e}")'''
m = m.replace(old_startup, new_startup)
open(r"files_extracted\main.py", "w", encoding="utf-8").write(m)
print("Fixed!")
