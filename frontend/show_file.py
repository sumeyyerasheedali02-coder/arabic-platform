import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
path = input("ادخلي مسار الملف: ")
print(open(path, encoding="utf-8").read())