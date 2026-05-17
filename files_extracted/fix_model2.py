m = open("main.py", encoding="utf-8").read()
m = m.replace("gemini-2.5-flash-preview-05-20", "gemini-2.0-flash")
open("main.py", "w", encoding="utf-8").write(m)
print("Done!")
