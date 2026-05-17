import os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("seed_database.py", encoding="utf-8").read()
old = "from book1_part1_data import BOOK_1_PART_1"
new = "from book1_part1_data import BOOK_1_PART_1\nfrom book1_part2_data import BOOK_1_PART_2"
if old in m:
    m = m.replace(old, new, 1)
    open("seed_database.py", "w", encoding="utf-8").write(m)
    print("Done!")
else:
    print("Pattern not found! Searching...")
    lines = m.split("\n")
    for i, l in enumerate(lines):
        if "book1_part1" in l:
            print(f"Line {i+1}: {repr(l)}")
