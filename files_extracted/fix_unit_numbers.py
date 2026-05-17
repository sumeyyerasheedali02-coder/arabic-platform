import os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("seed_database.py", encoding="utf-8").read()

# Change unit numbering for book 2 part 1
old = '        all_units = BOOK_1_PART_1["units"] + BOOK_1_PART_2["units"] + BOOK_2_PART_1["units"]'
new = '''        # Renumber units across books
        b1p1 = BOOK_1_PART_1["units"]
        b1p2 = BOOK_1_PART_2["units"]
        b2p1 = [dict(u, number=u["number"]+16) for u in BOOK_2_PART_1["units"]]
        all_units = b1p1 + b1p2 + b2p1'''

m = m.replace(old, new)
open("seed_database.py", "w", encoding="utf-8").write(m)
print("Done!")
