import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform")

m = open(r"files_extracted\main.py", encoding="utf-8").read()

seed_route = """
@app.get("/api/admin/seed")
async def run_seed(db: AsyncSession = Depends(get_db)):
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location("seed", "seed_database.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    import asyncio
    await mod.seed()
    return {"message": "Done!"}
"""

m = m.replace('if __name__ == "__main__":', seed_route + '\nif __name__ == "__main__":')
open(r"files_extracted\main.py", "w", encoding="utf-8").write(m)
print("Done!")
