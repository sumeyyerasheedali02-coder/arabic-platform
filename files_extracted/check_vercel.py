import sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = r"C:\Users\SD\Desktop\arabic_platform"
for folder in [root, os.path.join(root, "frontend")]:
    p = os.path.join(folder, "vercel.json")
    loc = "الجذر" if folder == root else "frontend"
    if os.path.exists(p):
        print(f"=== vercel.json ({loc}) موجود ===")
        print(open(p, encoding="utf-8").read())
    else:
        print(f"vercel.json ({loc}): غير موجود")