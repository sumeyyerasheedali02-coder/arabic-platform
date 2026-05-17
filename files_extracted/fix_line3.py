import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")
m = open("seed_database.py", encoding="utf-8").read()
lines = m.split("\n")
lines[1033] = "                    question_ar=ex[\"passage\"] + \"\\n\\n\" + ex[\"q\"],"
lines[1034] = ""
lines[1035] = ""
m = "\n".join(lines)
open("seed_database.py", "w", encoding="utf-8").write(m)
print("Done!")
