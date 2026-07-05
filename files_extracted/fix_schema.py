import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PATH = r"C:\Users\SD\Desktop\arabic_platform\files_extracted\schemas.py"
content = open(PATH, encoding="utf-8").read()

old = """    exercise_type:   str
    question_ar:     str"""

new = """    exercise_type:   str
    question_ar:     str
    correct_answer:  Optional[str] = None"""

if old in content:
    content = content.replace(old, new)
    open(PATH, "w", encoding="utf-8").write(content)
    print("✅ تم إضافة correct_answer إلى ExerciseOut")
else:
    print("⚠️ لم يُعثر على النص المتوقع")