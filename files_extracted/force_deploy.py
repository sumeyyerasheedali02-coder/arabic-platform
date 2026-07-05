import subprocess
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(f"$ {' '.join(cmd)}\n{r.stdout}{r.stderr}\n")

# تغيير بسيط لإجبار إعادة النشر
with open("main.py", "a", encoding="utf-8") as f:
    f.write("\n# redeploy trigger\n")

run(["git", "add", "main.py"])
run(["git", "commit", "-m", "chore: trigger redeploy"])
run(["git", "push"])
print("✅ تم. انتظري 3 دقائق ثم شغّلي verify.py")