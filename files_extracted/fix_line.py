import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")
m = open("seed_database.py", encoding="utf-8").read()

old = "                    question_ar=f\"{ex['passage']}\""
new = "                    question_ar=ex['passage'] + '\\n\\n' + ex['q'],"

m = m.replace(old, new)

# Also fix the next line that had the question
m = m.replace("                    correct_answer=ex[\"answer\"], options=ex.get(\"options\"),\n                    hint_ar=\"\u0627\u0633\u062a\u064a\u0639\u0627\u0628 \u0642\u0631\u0627\u0626\u064a\"",
              "                    correct_answer=ex[\"answer\"], options=ex.get(\"options\"),\n                    hint_ar=\"\u0627\u0633\u062a\u064a\u0639\u0627\u0628 \u0642\u0631\u0627\u0626\u064a\"")

open("seed_database.py", "w", encoding="utf-8").write(m)
print("Done!")
