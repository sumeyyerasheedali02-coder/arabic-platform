import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform")
m = open(r"files_extracted\main.py", encoding="utf-8").read()
new_endpoint = '''
@app.get("/api/run-seed")
async def run_seed_now():
    import traceback
    try:
        from seed_database import seed
        await seed()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "detail": str(e), "trace": traceback.format_exc()}
'''
m = m.replace('if __name__ == "__main__":', new_endpoint + '\nif __name__ == "__main__":')
open(r"files_extracted\main.py", "w", encoding="utf-8").write(m)
print("Done!")
