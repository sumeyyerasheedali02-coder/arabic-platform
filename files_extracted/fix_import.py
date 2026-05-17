import os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("seed_database.py", encoding="utf-8").read()
print("Has BOOK_1_PART_2 import:", "from book1_part2_data import" in m)
print("Has all_units:", "all_units" in m)

# Check lines around import
lines = m.split("\n")
for i, l in enumerate(lines):
    if "book1_part1" in l or "book1_part2" in l or "all_units" in l:
        print(f"Line {i+1}: {l}")
