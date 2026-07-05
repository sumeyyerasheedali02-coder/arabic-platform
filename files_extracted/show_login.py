import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
content = open(r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages\LoginRegister.jsx", encoding="utf-8").read()
idx = content.find("catch (err)")
print("=== معالجة الخطأ في handleSubmit ===")
print(repr(content[idx:idx+300]))