import os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("main.py", encoding="utf-8").read()

old = 'subprocess.run([sys.executable, "seed_database.py"], cwd="/app/files_extracted")'
new = 'pass  # seed via /api/admin/run-seed-now'
m = m.replace(old, new)

old2 = 'pass  # seed disabled on startup'
new2 = 'pass  # seed via /api/admin/run-seed-now'
m = m.replace(old2, new2)

open("main.py", "w", encoding="utf-8").write(m)
print("Done!")
