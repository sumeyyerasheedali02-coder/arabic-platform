m = open("main.py", encoding="utf-8").read()
new_ep = '''
@app.get("/api/admin/run-seed-now")
async def run_seed_now():
    try:
        from seed_database import seed
        await seed()
        return {"status": "success", "message": "Seed completed!"}
    except Exception as e:
        import traceback
        return {"status": "error", "detail": str(e), "trace": traceback.format_exc()}
'''
m = m.replace('if __name__ == "__main__":', new_ep + '\nif __name__ == "__main__":')
open("main.py", "w", encoding="utf-8").write(m)
print("Done!")
