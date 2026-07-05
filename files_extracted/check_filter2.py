import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
content = open(r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages\Exercises.jsx", encoding="utf-8").read()
# ابحث عن سطر word_order داخل matchesFilter (الثاني)
idx = content.find("matchesFilter")
seg = content[idx:idx+600]
# اطبع السطر الذي فيه word_order
for line in seg.split("\n"):
    if "word_order" in line or "رَتّ" in line or "رَتِّ" in line or "includes" in line:
        print(repr(line))