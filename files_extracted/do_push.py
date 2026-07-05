import subprocess

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(f"$ {' '.join(cmd)}")
    print(r.stdout)
    if r.stderr:
        print("stderr:", r.stderr)
    return r

# رفع main.py فقط (إصلاح الحوارات)
run(["git", "add", "main.py"])
run(["git", "commit", "-m", "fix: dialogues lazy-load using selectinload"])
run(["git", "push"])
print("\n✅ انتهى. انتظري 1-2 دقيقة حتى تُعيد Railway النشر تلقائياً.")