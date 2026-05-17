m = open("main.py", encoding="utf-8").read()
old = 'allow_origins=["https://arabic-platform-flame.vercel.app","http://localhost:5173","http://localhost:8003"],'
new = 'allow_origins=["*"],'
m = m.replace(old, new)
open("main.py", "w", encoding="utf-8").write(m)
print("Done!")
