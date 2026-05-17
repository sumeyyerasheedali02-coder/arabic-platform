import os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("seed_database.py", encoding="utf-8").read()
lines = m.split("\n")

# Find first import line and add after it
for i, line in enumerate(lines):
    if "from book1_part1_data" in line:
        print(f"Found at line {i+1}: {repr(line)}")
        lines.insert(i+1, "from book1_part2_data import BOOK_1_PART_2")
        m = "\n".join(lines)
        open("seed_database.py", "w", encoding="utf-8").write(m)
        print("Done!")
        break
else:
    print("Not found! Inserting at top...")
    m = "from book1_part2_data import BOOK_1_PART_2\n" + m
    open("seed_database.py", "w", encoding="utf-8").write(m)
    print("Done at top!")
