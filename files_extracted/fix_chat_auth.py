m = open("main.py", encoding="utf-8").read()
old = """@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(
    data:       ChatRequest,
    student_id: int = Depends(get_current_student),
    db:         AsyncSession = Depends(get_db)
):"""
new = """@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(
    data: ChatRequest,
    db:   AsyncSession = Depends(get_db)
):
    student_id = 0"""
m = m.replace(old, new)
open("main.py", "w", encoding="utf-8").write(m)
print("Done!")
