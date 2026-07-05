import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
content = open(r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages\Exercises.jsx", encoding="utf-8").read()
idx = content.find("{ value:")
start = content.rfind("[", 0, idx)
end = content.find("]", idx) + 1
print(content[start:end])