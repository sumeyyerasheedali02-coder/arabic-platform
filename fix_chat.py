import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages")
m = open("ArabicChat.jsx", encoding="utf-8").read()
m = m.replace('const API = "http://localhost:8003";', 'const API = import.meta.env.VITE_API_URL || "https://adaptable-solace-production-e226.up.railway.app";')
m = m.replace('`${API}/gemini/chat`', '`${API}/api/chat`')
m = m.replace('"message": text, "history": messages.map(m => ({ role: m.role, content: m.content }))', '"messages": messages.map(m => ({ role: m.role, content: m.content })).concat([{role:"user",content:text}])')
open("ArabicChat.jsx", "w", encoding="utf-8").write(m)
print("Done!")
