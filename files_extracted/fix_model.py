m = open("main.py", encoding="utf-8").read()
m = m.replace("gemini-1.5-flash", "gemini-2.5-flash-preview-05-20")
open("main.py", "w", encoding="utf-8").write(m)
print("Done!")
