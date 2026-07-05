import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform")

m = open(r"files_extracted\main.py", encoding="utf-8").read()

old = "@app.on_event(\"startup\")\nasync def startup():\n    await init_db()"

new = """@app.on_event(\"startup\")
async def startup():
    await init_db()
    async for db in get_db():
        result = await db.execute(select(Unit))
        unit = result.scalars().first()
        if not unit:
            from seed_database import seed
            await seed()
        break"""

m = m.replace(old, new)
open(r"files_extracted\main.py", "w", encoding="utf-8").write(m)
print("Done!")
