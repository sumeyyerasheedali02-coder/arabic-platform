m = open("main.py", encoding="utf-8").read()
old = '@app.post("/api/chat", response_model=ChatResponse)'
new = '''@app.options("/api/chat")
async def chat_options():
    from fastapi.responses import Response
    r = Response()
    r.headers["Access-Control-Allow-Origin"] = "*"
    r.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    r.headers["Access-Control-Allow-Headers"] = "*"
    return r

@app.post("/api/chat", response_model=ChatResponse)'''
m = m.replace(old, new)
open("main.py", "w", encoding="utf-8").write(m)
print("Done!")
