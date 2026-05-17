import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages")
m = open("ArabicChat.jsx", encoding="utf-8").read()
old = "const token = localStorage.getItem(\"token\");"
new = "const token = localStorage.getItem(\"token\") || \"\";"
m = m.replace(old, new)
# Fix Authorization header
old2 = "Authorization: `Bearer ${token}`"
new2 = "Authorization: token ? `Bearer ${token}` : \"\""
m = m.replace(old2, new2)
open("ArabicChat.jsx", "w", encoding="utf-8").write(m)
print("Done!")
