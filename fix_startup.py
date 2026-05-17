import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform")

m = open(r"files_extracted\main.py", encoding="utf-8").read()

old = "@app.on_event(\"startup\")\nasync def startup():\n    await init_db()"

new = "@app.on_event(\"startup\")\nasync def startup():\n    await init_db()\n    from sqlalchemy import text\n    async with AsyncSessionLocal() as db:\n        result = await db.execute(text(\"SELECT COUNT(*) FROM units\"))\n        count = result.scalar()\n        if count == 0:\n            import subprocess, sys\n            subprocess.run([sys.executable, \"seed_database.py\"], cwd=\"/app/files_extracted\")"

m = m.replace(old, new)
open(r"files_extracted\main.py", "w", encoding="utf-8").write(m)
print("Done!")
