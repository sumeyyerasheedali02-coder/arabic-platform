import sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

root = r"C:\Users\SD\Desktop\arabic_platform"

# ابحث عن ملفات إعداد Railway في الجذر والمجلد الفرعي
for name in ["railway.json", "railway.toml", "Procfile", "nixpacks.toml", "requirements.txt"]:
    for folder in [root, os.path.join(root, "files_extracted")]:
        p = os.path.join(folder, name)
        if os.path.exists(p):
            loc = "الجذر" if folder == root else "files_extracted"
            print(f"\n=== {name} ({loc}) ===")
            try:
                print(open(p, encoding="utf-8").read()[:500])
            except:
                print("(تعذر القراءة)")

# هل main.py في الجذر؟
print("\n=== main.py في الجذر؟ ===", os.path.exists(os.path.join(root, "main.py")))
print("=== main.py في files_extracted؟ ===", os.path.exists(os.path.join(root, "files_extracted", "main.py")))