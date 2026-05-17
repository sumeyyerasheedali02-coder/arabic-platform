import os

# Read book data
book_data = open("book1_part1_data.py", encoding="utf-8").read()

# Read seed file
seed = open("seed_database.py", encoding="utf-8").read()

# Replace import with embedded data
old = "from book1_part1_data import BOOK_1_PART_1"
new = book_data + "\n"

seed = seed.replace(old, new)
open("seed_database.py", "w", encoding="utf-8").write(seed)
print("Done! book data embedded in seed_database.py")
