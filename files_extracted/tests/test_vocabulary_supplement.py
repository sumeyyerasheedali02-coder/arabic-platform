"""Supplementary vocabulary: the data, and that adding it never touches student data."""
import re

import pytest
from sqlalchemy import select

from app import migrations
from app.services import vocabulary_supplement as supplement
from content.books import all_units
from content.vocabulary_supplement import SUPPLEMENT_VOCABULARY
from tools import add_vocabulary

from ._app import AsyncSessionLocal, Base, engine, models

ARABIC_ONLY = re.compile(r"^[؀-ۿ\s/؟]+$")
ARABIC_LETTER = re.compile(r"[ء-ي]")


# ── The data ──────────────────────────────────────────────────

def test_the_supplement_covers_units_1_to_32():
    assert sorted(SUPPLEMENT_VOCABULARY) == list(range(1, 33))


def test_every_entry_is_complete_and_clean():
    for number, words in SUPPLEMENT_VOCABULARY.items():
        for word in words:
            where = f"unit {number}: {word}"
            assert set(word) == {"word_ar", "word_tr", "word_en"}, where
            assert ARABIC_ONLY.match(word["word_ar"]), where
            assert word["word_tr"].strip() and word["word_en"].strip(), where
            assert not ARABIC_LETTER.search(word["word_tr"] + word["word_en"]), where
            for text in word.values():
                assert text == text.strip() and "  " not in text, where


def test_no_word_repeats_inside_a_unit():
    for number, words in SUPPLEMENT_VOCABULARY.items():
        seen = supplement.WordIndex()
        for word in words:
            assert not seen.has(word["word_ar"]), f"unit {number}: {word['word_ar']} twice"
            seen.add(word["word_ar"])


def test_against_the_base_content_every_unit_gains_words():
    base = {unit["number"]: [w["word_ar"] for w in unit["vocabulary"]] for unit in all_units()}
    plan = supplement.plan_additions(base)
    assert plan.missing_units == []
    assert sorted(plan.additions) == list(range(1, 33))
    assert all(len(words) >= 8 for words in plan.additions.values())
    assert plan.count >= 900


def test_words_are_compared_by_letters_and_by_vowels_when_both_have_them():
    same = supplement.same_word
    assert same("الكِتَاب", "كِتَابٌ")                # article and case ending ignored
    assert same("أَخ", "اخ")                          # one side without diacritics
    assert same("اشْتَرَى", "اِشْتَرَى")             # alif forms
    assert not same("رَأَى", "رَأْي")                  # saw / opinion
    assert not same("ظَهَرَ", "الظُّهْر")              # appeared / noon
    assert not same("حَمَى", "حُمَّى")                 # protected / fever
    assert not same("صَفَر", "صِفْر")                  # Safar / zero


def test_a_verb_entry_is_present_when_either_form_is():
    index = supplement.WordIndex(["يَقْرَأُ"])
    assert index.has_any_form("قَرَأَ / يَقْرَأُ")
    assert not index.has_any_form("كَتَبَ / يَكْتُبُ")


# ── The database ──────────────────────────────────────────────

async def _snapshot() -> dict:
    async with AsyncSessionLocal() as db:
        return {table.name: [tuple(row) for row in (await db.execute(
            select(table).order_by(*table.primary_key.columns))).all()]
            for table in Base.metadata.sorted_tables}


async def _run(apply: bool):
    async with engine.begin() as conn:
        return await supplement.add_supplementary_vocabulary(conn, apply=apply)


async def _student_with_history(client, register, content):
    """A student with review cards, an answer, progress and a rated card."""
    student = await register()
    await client.post(f"/api/me/srs/add-unit/{content.unit_a}", headers=student.headers)
    await client.post("/api/me/srs/review", headers=student.headers,
                      json={"vocabulary_id": content.vocab_a[0], "quality": 4})
    async with AsyncSessionLocal() as db:
        db.add_all([
            models.ExerciseAnswer(student_id=student.id, exercise_id=content.ex_choice,
                                  student_answer="kitap", is_correct=True, points_earned=10),
            models.StudentProgress(student_id=student.id, unit_id=content.unit_a,
                                   lesson_id=content.a_muf, status="completed", score=90,
                                   attempts=2, time_spent_sec=120),
        ])
        await db.commit()
    return student


async def test_adding_the_words_changes_nothing_that_already_exists(client, register, content):
    student = await _student_with_history(client, register, content)
    before = await _snapshot()

    result = await _run(apply=True)

    after = await _snapshot()
    assert result.applied and result.plan.count > 20
    for table, rows in before.items():
        if table == "vocabulary":
            assert all(row in after[table] for row in rows), "an existing word changed or vanished"
        else:
            assert after[table] == rows, f"{table} changed"
    assert len(after["vocabulary"]) == len(before["vocabulary"]) + result.plan.count
    assert result.vocabulary_after - result.vocabulary_before == result.plan.count

    # the student's own data is exactly as it was
    due = await client.get("/api/me/srs/due", headers=student.headers)
    assert due.status_code == 200
    cards = [row for row in after["srs_cards"] if row[1] == student.id]
    assert len(cards) == len(content.vocab_a)           # no card was created for a new word


async def test_new_words_belong_to_the_units_vocabulary_lesson(content):
    result = await _run(apply=True)
    assert set(result.plan.additions) >= {1, 2}

    async with AsyncSessionLocal() as db:
        new_rows = (await db.execute(select(models.Vocabulary).where(
            models.Vocabulary.id > result.highest_id_before).order_by(models.Vocabulary.id))).scalars().all()
    assert len(new_rows) == result.plan.count
    lesson_of = {content.unit_a: content.a_muf, content.unit_b: content.b_muf}
    for row in new_rows:
        assert row.lesson_id == lesson_of[row.unit_id]
        assert row.difficulty == 1 and row.word_ar and row.translation_tr and row.translation_en


async def test_running_it_again_adds_nothing(content):
    first = await _run(apply=True)
    snapshot = await _snapshot()
    second = await _run(apply=True)
    assert first.plan.count > 0
    assert second.plan.count == 0 and not second.applied
    assert await _snapshot() == snapshot


async def test_a_dry_run_writes_nothing(content):
    snapshot = await _snapshot()
    result = await _run(apply=False)
    assert result.plan.count > 20 and not result.applied
    assert await _snapshot() == snapshot


async def test_units_missing_from_the_database_are_skipped(content):
    result = await _run(apply=False)
    assert result.plan.missing_units == list(range(3, 33))


async def test_students_can_study_the_new_words(client, register, content):
    student = await register()
    before = await client.get(f"/api/units/{content.unit_a}/vocabulary")
    result = await _run(apply=True)
    after = await client.get(f"/api/units/{content.unit_a}/vocabulary")
    added = len(result.plan.additions[1])
    assert len(after.json()) == len(before.json()) + added

    res = await client.post(f"/api/me/srs/add-unit/{content.unit_a}", headers=student.headers)
    assert res.json()["added"] == len(before.json()) + added


async def test_the_command_line_tool_reports_without_changing_anything(content, capsys):
    snapshot = await _snapshot()
    totals = await add_vocabulary.run(apply=False, log=print)
    assert totals["to_add"] > 20
    assert await _snapshot() == snapshot
    assert "Dry run, nothing was changed" in capsys.readouterr().out


# ── Migration 0010 ────────────────────────────────────────────

def test_the_migration_is_registered_last():
    assert migrations.MIGRATIONS[-1][0] == "0010_supplementary_vocabulary"


async def test_the_migration_adds_the_words(content):
    async with engine.begin() as conn:
        await migrations._add_supplementary_vocabulary(conn)
    async with AsyncSessionLocal() as db:
        count = (await db.execute(select(models.Vocabulary))).scalars().all()
    assert len(count) > len(content.vocab_a) + len(content.vocab_b) + 20


async def test_a_failing_migration_leaves_the_database_exactly_as_it_was(content, monkeypatch):
    original = supplement.add_supplementary_vocabulary

    async def insert_then_fail(conn, **kwargs):
        await original(conn, **kwargs)           # rows are inserted ...
        raise RuntimeError("simulated failure")  # ... and then it breaks

    monkeypatch.setattr(supplement, "add_supplementary_vocabulary", insert_then_fail)
    snapshot = await _snapshot()
    async with engine.begin() as conn:
        await migrations._add_supplementary_vocabulary(conn)   # must not raise
    assert await _snapshot() == snapshot


@pytest.mark.parametrize("apply", [False, True])
async def test_an_empty_database_is_left_alone(apply):
    async with AsyncSessionLocal() as db:
        for table in reversed(Base.metadata.sorted_tables):
            await db.execute(table.delete())
        await db.commit()
    result = await _run(apply=apply)
    assert result.plan.count == 0 and not result.applied
    assert result.plan.missing_units == list(range(1, 33))
