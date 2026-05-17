content = open("seed_database.py", encoding="utf-8").read()
old = 'os.path.join(os.path.dirname(__file__), "..", "book1_part1_data.py")'
new = 'os.path.join(os.path.dirname(os.path.abspath(__file__)), "book1_part1_data.py")'
content = content.replace(old, new)
open("seed_database.py", "w", encoding="utf-8").write(content)
print("Fixed!")
print("New path line:")
for line in content.split("\n"):
    if "book1_part1" in line:
        print(line)
