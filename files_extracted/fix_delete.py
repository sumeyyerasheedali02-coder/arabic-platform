import os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("seed_database.py", encoding="utf-8").read()

# Check current delete tables
lines = m.split("\n")
for i, l in enumerate(lines):
    if "DELETE FROM" in l or "delete from" in l.lower():
        print(f"Line {i+1}: {l}")
