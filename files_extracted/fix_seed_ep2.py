import os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("main.py", encoding="utf-8").read()

old = '''@app.get("/api/admin/run-seed-now")
async def run_seed_now():'''

new = '''@app.get("/api/admin/run-seed-now")
async def run_seed_now_fixed():'''

m = m.replace(old, new)

# Fix the pass inside run-seed-now endpoint
lines = m.split("\n")
in_endpoint = False
for i, line in enumerate(lines):
    if "async def run_seed_now_fixed" in line:
        in_endpoint = True
    if in_endpoint and "pass  # seed via" in line:
        lines[i] = lines[i].replace(
            "pass  # seed via /api/admin/run-seed-now",
            'from seed_database import seed\n        await seed()\n        return {"status": "success", "message": "Seed completed!"}'
        )
        in_endpoint = False
        break

m = "\n".join(lines)
open("main.py", "w", encoding="utf-8").write(m)
print("Done!")
