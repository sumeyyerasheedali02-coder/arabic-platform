import os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("seed_database.py", encoding="utf-8").read()

lines = m.split("\n")
for i, l in enumerate(lines):
    if i >= 830 and i <= 860:
        print(f"{i+1}: {repr(l)}")
