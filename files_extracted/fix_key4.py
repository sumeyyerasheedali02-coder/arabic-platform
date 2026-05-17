m = open("main.py", encoding="utf-8").read()
m = m.replace("AIzaSyDGF2FgKVVvsEqKbGhJ-aYKCHxpA9ikzmk", "AIzaSyBy9MGRLtBFgI3JQ04w1MsO5-Ap5EYuoHo")
open("main.py", "w", encoding="utf-8").write(m)
print("Done!")
