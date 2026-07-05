import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
content = open(r"C:\Users\SD\Desktop\arabic_platform\files_extracted\schemas.py", encoding="utf-8").read()
idx = content.find("class ExerciseOut")
print(content[idx:idx+400])