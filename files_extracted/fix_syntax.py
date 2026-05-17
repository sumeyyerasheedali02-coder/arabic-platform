import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")
m = open("seed_database.py", encoding="utf-8").read()
lines = m.split("\n")
print(f"Line 1034: {repr(lines[1033])}")
print(f"Line 1033: {repr(lines[1032])}")
print(f"Line 1035: {repr(lines[1034])}")
