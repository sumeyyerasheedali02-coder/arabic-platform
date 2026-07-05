import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
content = open(r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages\Exercises.jsx", encoding="utf-8").read()
idx = content.find("if (isGuest)")
print(content[max(0,idx-200):idx+800])