import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
content = open("main.py", encoding="utf-8").read()
idx = content.find("async def startup")
print(content[idx:idx+900])