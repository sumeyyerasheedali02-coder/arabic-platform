import os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("seed_database.py", encoding="utf-8").read()

if "book1_part2_data" in m:
    print("Already added!")
else:
    old = "from book1_part1_data import BOOK_1_PART_1"
    new = "from book1_part1_data import BOOK_1_PART_1\nfrom book1_part2_data import BOOK_1_PART_2"
    m = m.replace(old, new, 1)

    old2 = "        for u_data in BOOK_1_PART_1[\"units\"]:"
    new2 = "        all_units = BOOK_1_PART_1[\"units\"] + BOOK_1_PART_2[\"units\"]\n        for u_data in all_units:"
    m = m.replace(old2, new2, 1)

    open("seed_database.py", "w", encoding="utf-8").write(m)
    print("Done!")
