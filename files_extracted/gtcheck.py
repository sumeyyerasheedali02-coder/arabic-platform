import subprocess
r = subprocess.run(["git", "diff", "main.py"], capture_output=True, text=True, encoding="utf-8")
print(r.stdout[:3000])