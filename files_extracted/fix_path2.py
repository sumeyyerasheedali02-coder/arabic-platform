content = open("seed_database.py", encoding="utf-8").read()
old = """import importlib.util
_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "book1_part1_data.py")
_spec = importlib.util.spec_from_file_location("book1_part1_data", os.path.abspath(_data_path))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
BOOK_1_PART_1 = _mod.BOOK_1_PART_1"""
new = "from book1_part1_data import BOOK_1_PART_1"
content = content.replace(old, new)
open("seed_database.py", "w", encoding="utf-8").write(content)
print("Fixed!")
