import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")
m = open("seed_database.py", encoding="utf-8").read()
lines = m.split("\n")
# Show lines around 1034
for i in range(1030, 1040):
    print(f"{i+1}: {repr(lines[i])}")
