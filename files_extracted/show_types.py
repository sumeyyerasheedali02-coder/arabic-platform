import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
content = open(r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages\Exercises.jsx", encoding="utf-8").read()

# ابحث عن أسماء الأنواع المذكورة
for keyword in ["متعاكس", "مترادف", "الجمع", "استيعاب", "ترتيب", "antonym", "synonym", "plural", "comprehension", "order", "opposite"]:
    idx = content.find(keyword)
    if idx > 0:
        print(f"'{keyword}' موجود عند {idx}:")
        print("   ", content[idx-60:idx+60].replace("\n", " "))
        print()