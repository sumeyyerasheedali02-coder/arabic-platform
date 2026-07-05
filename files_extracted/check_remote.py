import subprocess
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(f"$ {' '.join(cmd)}\n{r.stdout}{r.stderr}\n")

run(["git", "log", "--oneline", "-3"])
run(["git", "status"])