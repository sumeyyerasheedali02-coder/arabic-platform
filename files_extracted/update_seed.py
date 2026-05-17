import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("seed_database.py", encoding="utf-8").read()

if "exercises_data" in m:
    print("Already has exercises_data!")
else:
    # Add import after "from database import"
    old = "from database import ("
    new = "from exercises_data import EXERCISES_DATA\nfrom database import ("
    m = m.replace(old, new, 1)
    open("seed_database.py", "w", encoding="utf-8").write(m)
    print("Added import!")
