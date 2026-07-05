import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
content = open("main.py", encoding="utf-8").read()

print("=== فحص الاستيراد ===")
print("selectinload موجود؟", "selectinload" in content)

# أظهر أول 40 سطر لرؤية الاستيرادات
print("\n=== أول الاستيرادات ===")
for i, line in enumerate(content.split("\n")[:40], 1):
    if "import" in line or "selectinload" in line:
        print(f"{i}: {line}")

# أظهر دالة الحوارات الحالية
print("\n=== دالة الحوارات الحالية ===")
idx = content.find("async def get_dialogues")
print(content[idx:idx+450])