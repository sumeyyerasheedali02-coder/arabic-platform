"""
Seed database with Book 1 Part 1 — 8 real units from العربية بين يديك.
Run once on a fresh database or to replace all content:
    python seed_database.py
Students are preserved; all content + progress tables are wiped and rebuilt.
"""
import asyncio
import sys
import os
import random
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from sqlalchemy import text, select
from database import (
    init_db, AsyncSessionLocal,
    Unit, Lesson, Vocabulary, Dialogue, DialogueLine, Exercise,
    SRSCard, Student, StudentProgress, ExerciseAnswer,
)

# Copy book data file into the backend directory if needed
import importlib.util
_data_path = os.path.join(os.path.dirname(__file__), "..", "book1_part1_data.py")
_spec = importlib.util.spec_from_file_location("book1_part1_data", os.path.abspath(_data_path))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
BOOK_1_PART_1 = _mod.BOOK_1_PART_1


async def seed():
    await init_db()
    async with AsyncSessionLocal() as db:

        # ── Wipe content + activity (keep student accounts) ───────────
        for table in [
            "srs_cards", "exercise_answers", "student_progress",
            "exercises", "dialogue_lines", "dialogues",
            "vocabulary", "lessons", "units",
        ]:
            await db.execute(text(f"DELETE FROM {table}"))
        await db.commit()
        print("Cleared existing content.")

        # ── Fetch existing students for SRS card creation ──────────────
        result = await db.execute(select(Student))
        students = result.scalars().all()
        print(f"Found {len(students)} existing student(s).")

        all_vocab_ids = []

        for u_data in BOOK_1_PART_1["units"]:
            grammar_text = " | ".join(u_data["grammar"])
            topics_text  = " | ".join(u_data["main_topics"])

            unit = Unit(
                unit_number    = u_data["number"],
                title_ar       = u_data["title_ar"],
                title_tr       = u_data["title_tr"],
                description_ar = topics_text,
                description_tr = u_data["title_tr"],
                total_lessons  = 3,
            )
            db.add(unit)
            await db.flush()
            print(f"\n  Unit {unit.unit_number}: {unit.title_ar}  (id={unit.id})")

            # ── 3 lessons per unit ─────────────────────────────────────
            lesson_hiwar = Lesson(
                unit_id       = unit.id,
                lesson_number = 1,
                title_ar      = "الحِوَارَات",
                title_tr      = "Diyaloglar",
                lesson_type   = "hiwar",
            )
            lesson_mufradat = Lesson(
                unit_id       = unit.id,
                lesson_number = 2,
                title_ar      = "المُفْرَدَات",
                title_tr      = "Kelimeler",
                lesson_type   = "mufradat",
            )
            lesson_nahw = Lesson(
                unit_id       = unit.id,
                lesson_number = 3,
                title_ar      = "النَّحْو وَالتَّرَاكِيب",
                title_tr      = "Dilbilgisi",
                lesson_type   = "nahw",
                grammar_focus = grammar_text,
            )
            db.add_all([lesson_hiwar, lesson_mufradat, lesson_nahw])
            await db.flush()

            # ── Dialogues ─────────────────────────────────────────────
            for i, d in enumerate(u_data["dialogues"]):
                dialogue = Dialogue(
                    lesson_id       = lesson_hiwar.id,
                    dialogue_number = i + 1,
                    title_ar        = d["title"],
                    situation_tr    = "، ".join(d["speakers"]),
                )
                db.add(dialogue)
                await db.flush()
                for j, line in enumerate(d["lines"]):
                    db.add(DialogueLine(
                        dialogue_id    = dialogue.id,
                        line_order     = j + 1,
                        speaker        = line["speaker"],
                        text_ar        = line["text"],
                        translation_tr = None,
                        is_key_phrase  = False,
                    ))
            await db.flush()
            print(f"    dialogues : {len(u_data['dialogues'])}")

            # ── Vocabulary ────────────────────────────────────────────
            vocab_list = u_data["vocabulary"]
            new_vocab_ids = []
            for v in vocab_list:
                vocab = Vocabulary(
                    unit_id        = unit.id,
                    lesson_id      = lesson_mufradat.id,
                    word_ar        = v["word_ar"],
                    translation_tr = v["word_tr"],
                    translation_en = v["word_en"],
                    difficulty     = 1,
                )
                db.add(vocab)
                await db.flush()
                new_vocab_ids.append(vocab.id)
            all_vocab_ids.extend(zip([unit.id] * len(new_vocab_ids), new_vocab_ids))
            print(f"    vocabulary: {len(vocab_list)} words")

            # ── Exercises (auto-generated from vocabulary) ────────────
            ex_num = 0
            for i, v in enumerate(vocab_list):
                others = [x["word_tr"] for x in vocab_list if x["word_tr"] != v["word_tr"]]
                wrong  = random.sample(others, min(3, len(others)))
                opts   = wrong + [v["word_tr"]]
                random.shuffle(opts)

                ex_num += 1
                db.add(Exercise(
                    unit_id         = unit.id,
                    lesson_id       = lesson_mufradat.id,
                    exercise_number = ex_num,
                    exercise_type   = "multiple_choice",
                    question_ar     = f"مَا مَعْنَى كَلِمَة: {v['word_ar']}؟",
                    correct_answer  = v["word_tr"],
                    options         = opts,
                    difficulty      = 1,
                    points          = 10,
                ))

                # true/false — alternate correct/wrong to keep balance
                if i % 2 == 0:
                    shown_tr   = v["word_tr"]
                    correct_tf = "صَحِيح"
                else:
                    other_list = [x["word_tr"] for x in vocab_list if x["word_tr"] != v["word_tr"]]
                    shown_tr   = random.choice(other_list) if other_list else v["word_tr"]
                    correct_tf = "خَطَأ"

                ex_num += 1
                db.add(Exercise(
                    unit_id         = unit.id,
                    lesson_id       = lesson_mufradat.id,
                    exercise_number = ex_num,
                    exercise_type   = "true_false",
                    question_ar     = f"هَلْ مَعْنَى «{v['word_ar']}» بِالتُّرْكِيَّة: «{shown_tr}»؟",
                    correct_answer  = correct_tf,
                    options         = ["صَحِيح", "خَطَأ"],
                    difficulty      = 1,
                    points          = 5,
                ))

            await db.flush()
            print(f"    exercises : {ex_num}")

        # ── SRS cards for every student × every vocab word ─────────────
        today = date.today().isoformat()
        srs_count = 0
        for student in students:
            for _unit_id, vocab_id in all_vocab_ids:
                db.add(SRSCard(
                    student_id    = student.id,
                    vocabulary_id = vocab_id,
                    ease_factor   = 2.5,
                    interval_days = 1,
                    repetitions   = 0,
                    next_review   = today,
                ))
                srs_count += 1

        await db.flush()
        await db.commit()
        print(f"\n  SRS cards : {srs_count} ({len(students)} students × {len(all_vocab_ids)} words)")
        print("\nDone! Database seeded with Book 1 Part 1 (8 units).")


if __name__ == "__main__":
    asyncio.run(seed())
