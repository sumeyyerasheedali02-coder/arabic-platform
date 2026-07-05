import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PATH = r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages\LoginRegister.jsx"
content = open(PATH, encoding="utf-8").read()

# اعرض كل الألوان المستخدمة
colors = re.findall(r"color:\s*['\"]([#\w]+)['\"]", content)
bgs = re.findall(r"background:\s*['\"]([^'\"]+)['\"]", content)
borders = re.findall(r"borderColor:\s*['\"]([^'\"]+)['\"]", content)

print("=== الألوان ===")
for c in sorted(set(colors)):
    print(f"  {c}")
print("\n=== الخلفيات ===")
for b in sorted(set(bgs)):
    print(f"  {b}")
print("\n=== الحدود ===")
for b in sorted(set(borders)):
    print(f"  {b}")