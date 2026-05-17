import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform")

m = open(r"files_extracted\main.py", encoding="utf-8").read()

old = "@app.on_event(\"startup\")\nasync def startup():\n    await init_db()"

new = "@app.on_event(\"startup\")\nasync def startup():\n    await init_db()\n    try:\n        from seed_database import seed\n        await seed()\n        print(\"Seed completed successfully\")\n    except Exception as e:\n        print(f\"Seed error: {e}\")"

m = m.replace(old, new)
open(r"files_extracted\main.py", "w", encoding="utf-8").write(m)
print("Done!")
