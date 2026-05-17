import os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("main.py", encoding="utf-8").read()

# Check if seed runs on startup
if "await seed()" in m and "startup" in m:
    print("Seed runs on startup - this causes timeout!")
    # Remove seed from startup
    m = m.replace("    await seed()\n", "    pass  # seed disabled on startup\n")
    open("main.py", "w", encoding="utf-8").write(m)
    print("Fixed!")
else:
    print("Seed not in startup")
    # Show relevant lines
    lines = m.split("\n")
    for i, l in enumerate(lines):
        if "seed" in l.lower() and "startup" not in l.lower():
            print(f"Line {i+1}: {l}")
