import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform")
m = open(r"files_extracted\main.py", encoding="utf-8").read()
old = '''@app.on_event("startup")
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
new = '''@app.on_event("startup")
async def startup():
    await init_db()
    from seed_database import seed
    await seed()'''
m = m.replace(old, new)
open(r"files_extracted\main.py", "w", encoding="utf-8").write(m)
print("Done!")
