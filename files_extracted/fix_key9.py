m = open("main.py", encoding="utf-8").read()
m = m.replace("AIzaSyCzfVZAgO6GKFMgvPphTUZJvhuv0HyLF9U", "AIzaSyB0ceyGlZHh2FShXJS3cgQKqwU0pQk992U")
open("main.py", "w", encoding="utf-8").write(m)
print("Done!")
