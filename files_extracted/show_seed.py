import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
content = open("seed_database.py", encoding="utf-8").read()

# ابحث عن توليد التمارين
for kw in ["exercise_type", "multiple_choice", "Exercise(", "أضداد", "عكس", "جمع"]:
    idx = content.find(kw)
    if idx > 0:
        print(f"=== '{kw}' عند {idx} ===")
        print(content[idx-100:idx+200])
        print()