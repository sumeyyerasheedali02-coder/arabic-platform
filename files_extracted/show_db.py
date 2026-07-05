import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
content = open("database.py", encoding="utf-8").read()
idx = content.find("class DialogueLine")
print(content[idx:idx+700])