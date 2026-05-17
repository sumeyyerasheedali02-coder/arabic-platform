m = open("main.py", encoding="utf-8").read()
m = m.replace("api_key=os.getenv('GOOGLE_API_KEY')", "api_key='AIzaSyCdMIFinbWLs3c6ZjyDXNPGGgRMzS5umGU'")
open("main.py", "w", encoding="utf-8").write(m)
print("Done!")
