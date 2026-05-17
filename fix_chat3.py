import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages")
m = open("ArabicChat.jsx", encoding="utf-8").read()
old = 'body: JSON.stringify({ message: text, history: messages.map(m => ({ role: m.role, content: m.content })) }),'
new = 'body: JSON.stringify({ messages: [...messages, {role:"user",content:text}].map(m => ({ role: m.role, content: m.content })) }),'
m = m.replace(old, new)
open("ArabicChat.jsx", "w", encoding="utf-8").write(m)
print("Done! replaced:", old in open("ArabicChat.jsx").read())
