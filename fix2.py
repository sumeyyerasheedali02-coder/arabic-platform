import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform")

# اقر seed_database.py
seed = open(r"files_extracted\seed_database.py", encoding="utf-8").read()
print("seed_database.py content:")
print(seed[:500])
print("...")
print(seed[-500:])
