import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform")

# Fix database.py to use PostgreSQL
db_content = open(r"files_extracted\database.py", encoding="utf-8").read()
print("Current DB URL line:")
for line in db_content.split("\n"):
    if "sqlite" in line.lower() or "database_url" in line.lower() or "engine" in line.lower():
        print(repr(line))
