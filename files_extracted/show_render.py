import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
content = open(r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages\Exercises.jsx", encoding="utf-8").read()

idx = content.find("'true_false'")
print(content[idx-20:idx+800])