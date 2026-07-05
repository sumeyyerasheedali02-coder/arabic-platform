import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
content = open("main.py", encoding="utf-8").read()
idx = content.find("async def get_dialogues")
# اعرض من بداية الديكوريتر قبلها
start = content.rfind("@app", 0, idx)
print(content[start:idx+500])