import os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("main.py", encoding="utf-8").read()
print("run-seed-now in main.py:", "run-seed-now" in m)

lines = m.split("\n")
for i, l in enumerate(lines):
    if "run-seed" in l or "run_seed" in l or "admin" in l:
        print(f"Line {i+1}: {l}")
