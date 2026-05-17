import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("seed_database.py", encoding="utf-8").read()

old = "            await db.flush()\n            print(f\"    exercises : {ex_num}\")"

new = """            # fill_blank
            unit_ex = EXERCISES_DATA.get(u_data["number"], {})
            for ex in unit_ex.get("fill_blank", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_hiwar.id,
                    exercise_number=ex_num, exercise_type="fill_blank",
                    question_ar=ex["q"], correct_answer=ex["answer"],
                    hint_ar=ex.get("hint"), options=None, difficulty=2, points=10))
            # translate_ar_tr
            for ex in unit_ex.get("translate_ar_tr", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_mufradat.id,
                    exercise_number=ex_num, exercise_type="translate_ar_tr",
                    question_ar=f"\u062a\u0631\u062c\u0645 \u0625\u0644\u0649 \u0627\u0644\u062a\u0631\u0643\u064a\u0629: {ex['q']}",
                    correct_answer=ex["answer"], options=ex.get("options"), difficulty=2, points=10))
            # translate_tr_ar
            for ex in unit_ex.get("translate_tr_ar", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_mufradat.id,
                    exercise_number=ex_num, exercise_type="translate_tr_ar",
                    question_ar=f"\u062a\u0631\u062c\u0645 \u0625\u0644\u0649 \u0627\u0644\u0639\u0631\u0628\u064a\u0629: {ex['q']}",
                    correct_answer=ex["answer"], options=ex.get("options"), difficulty=2, points=10))
            # match
            for match_data in unit_ex.get("match", []):
                for pair in match_data["pairs"]:
                    others = [p["tr"] for p in match_data["pairs"] if p["tr"] != pair["tr"]]
                    import random as rnd
                    wrong = rnd.sample(others, min(3, len(others)))
                    opts = wrong + [pair["tr"]]
                    rnd.shuffle(opts)
                    ex_num += 1
                    db.add(Exercise(unit_id=unit.id, lesson_id=lesson_mufradat.id,
                        exercise_number=ex_num, exercise_type="match",
                        question_ar=f"\u0635\u0644: {pair['ar']}",
                        correct_answer=pair["tr"], options=opts, difficulty=1, points=5))
            # synonyms
            for ex in unit_ex.get("synonyms", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_nahw.id,
                    exercise_number=ex_num, exercise_type="multiple_choice",
                    question_ar=ex["q"], correct_answer=ex["answer"],
                    options=ex.get("options"), hint_ar="\u0645\u062a\u0631\u0627\u062f\u0641", difficulty=3, points=15))
            # antonyms
            for ex in unit_ex.get("antonyms", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_nahw.id,
                    exercise_number=ex_num, exercise_type="multiple_choice",
                    question_ar=ex["q"], correct_answer=ex["answer"],
                    options=ex.get("options"), hint_ar="\u0636\u062f / \u0645\u062a\u0639\u0627\u0643\u0633", difficulty=3, points=15))
            # word_order
            for ex in unit_ex.get("word_order", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_hiwar.id,
                    exercise_number=ex_num, exercise_type="fill_blank",
                    question_ar=f"\u0631\u064e\u062a\u0651\u0650\u0628 \u0627\u0644\u0643\u0644\u0645\u0627\u062a: {' / '.join(ex['words'])}",
                    correct_answer=ex["answer"], hint_ar=ex.get("hint"),
                    options=None, difficulty=3, points=15))
            # comprehension
            for ex in unit_ex.get("comprehension", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_hiwar.id,
                    exercise_number=ex_num, exercise_type="multiple_choice",
                    question_ar=f"{ex['passage']}\n\n{ex['q']}",
                    correct_answer=ex["answer"], options=ex.get("options"),
                    hint_ar="\u0627\u0633\u062a\u064a\u0639\u0627\u0628 \u0642\u0631\u0627\u0626\u064a", difficulty=3, points=20))
            # plural
            for ex in unit_ex.get("plural", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_nahw.id,
                    exercise_number=ex_num, exercise_type="multiple_choice",
                    question_ar=ex["q"], correct_answer=ex["answer"],
                    options=ex.get("options"), hint_ar="\u062c\u0645\u0639 \u0627\u0644\u0643\u0644\u0645\u0629", difficulty=3, points=15))

            await db.flush()
            print(f"    exercises : {ex_num}")"""

if old in m:
    m = m.replace(old, new)
    open("seed_database.py", "w", encoding="utf-8").write(m)
    print("Done!")
else:
    print("Pattern not found!")
    idx = m.find("print(f\"    exercises")
    print(repr(m[idx-50:idx+50]))
