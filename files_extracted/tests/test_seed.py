"""Content loading: guarded, transactional, and never reachable over HTTP."""
import dataclasses
import random

import pytest
from sqlalchemy import func, select

from tools import seed as seed_tool

from ._app import AsyncSessionLocal, main_module, models

TINY_UNITS = [
    {
        "number": number,
        "title_ar": f"وحدة {number}", "title_tr": f"Ünite {number}",
        "main_topics": ["موضوع أول", "موضوع ثان"],
        "grammar": ["قاعدة أولى", "قاعدة ثانية"],
        "dialogues": [{"title": "حوار", "speakers": ["أ", "ب"],
                       "lines": [{"speaker": "أ", "text": "مرحبا"}, {"speaker": "ب", "text": "أهلا"}]}],
        "vocabulary": [{"word_ar": f"كلمة{number}-{i}", "word_tr": f"kelime{number}-{i}",
                        "word_en": f"word{number}-{i}"} for i in range(1, 7)],
    }
    for number in (1, 9)
]
TINY_EXERCISES = {1: {
    "fill_blank": [{"q": "السلام ___", "answer": "عليكم", "hint": "تحية"}],
    "synonyms": [{"q": "مرادف: مدرس؟", "answer": "أستاذ", "options": ["أستاذ", "طالب"]}],
    "word_order": [{"words": ["خالد", "اسمي"], "answer": "اسمي خالد"}],
}}


async def _count(model, *where):
    async with AsyncSessionLocal() as db:
        return (await db.execute(select(func.count()).select_from(model).where(*where))).scalar()


async def _empty_content():
    async with AsyncSessionLocal() as db:
        for model in (models.Exercise, models.DialogueLine, models.Dialogue,
                      models.Vocabulary, models.Lesson, models.Unit):
            await db.execute(model.__table__.delete())
        await db.commit()


def _quiet(*args):
    pass


@pytest.mark.parametrize("path", ["/api/admin/seed", "/api/admin/run-seed-now", "/api/run-seed"])
async def test_seeding_is_not_exposed_over_http(client, seed_spy, path):
    res = await client.get(path)
    assert res.status_code == 404
    assert seed_spy == []


async def test_seed_refuses_to_touch_a_database_that_has_content(register, client, content):
    student = await register()
    await client.post(f"/api/me/srs/add-unit/{content.unit_a}", headers=student.headers)

    with pytest.raises(seed_tool.ContentExistsError):
        await seed_tool.seed(units=TINY_UNITS, log=_quiet)

    assert (await _count(models.SRSCard), await _count(models.Unit)) == (4, 2)


def test_replacing_content_from_the_command_line_needs_explicit_confirmation(seed_spy):
    with pytest.raises(SystemExit) as exit_info:
        seed_tool.main(["--replace"])
    assert exit_info.value.code == 2
    assert seed_spy == []


async def test_startup_never_seeds_a_database_that_has_content(seed_spy):
    await main_module.on_startup()
    assert seed_spy == []


async def test_startup_bootstraps_only_an_empty_database_and_can_be_disabled(seed_spy, monkeypatch):
    await _empty_content()

    disabled = dataclasses.replace(main_module.settings, seed_on_empty_db=False)
    monkeypatch.setattr(main_module, "settings", disabled)
    await main_module.on_startup()
    assert seed_spy == []

    enabled = dataclasses.replace(main_module.settings, seed_on_empty_db=True)
    monkeypatch.setattr(main_module, "settings", enabled)
    await main_module.on_startup()
    assert len(seed_spy) == 1
    assert not seed_spy[0][1].get("replace") and not seed_spy[0][1].get("with_supplements")


async def test_base_content_layout(client):
    await _empty_content()
    totals = await seed_tool.seed(units=TINY_UNITS, unit_exercises=TINY_EXERCISES,
                                  rng=random.Random(1), log=_quiet)
    # 6 words -> 12 generated exercises per unit; unit 1 has 3 hand-written ones on top
    assert totals == {"units": 2, "lessons": 6, "dialogues": 2, "vocabulary": 12, "exercises": 27}

    units = (await client.get("/api/units")).json()
    assert [(u["unit_number"], u["total_lessons"]) for u in units] == [(1, 3), (9, 3)]
    assert units[0]["description_ar"] == "موضوع أول | موضوع ثان"

    lessons = (await client.get(f"/api/units/{units[0]['id']}/lessons")).json()
    assert [(item["lesson_number"], item["lesson_type"]) for item in lessons] == [
        (1, "hiwar"), (2, "mufradat"), (3, "nahw")]
    assert lessons[2]["grammar_focus"] == "قاعدة أولى | قاعدة ثانية"

    dialogue = (await client.get(f"/api/lessons/{lessons[0]['id']}/dialogues")).json()[0]
    assert dialogue["situation_tr"] == "أ، ب"
    assert [line["text_ar"] for line in dialogue["lines"]] == ["مرحبا", "أهلا"]

    exercises = (await client.get(f"/api/units/{units[0]['id']}/exercises")).json()
    assert [e["exercise_number"] for e in exercises] == list(range(1, 16))
    choice, true_false = exercises[0], exercises[1]
    assert choice["exercise_type"] == "multiple_choice" and choice["points"] == 10
    assert choice["correct_answer"] in choice["options"] and len(choice["options"]) == 4
    assert true_false["options"] == ["صَحِيح", "خَطَأ"] and true_false["points"] == 5
    by_lesson = {item["lesson_type"]: item["id"] for item in lessons}
    blank, synonym, order = exercises[12], exercises[13], exercises[14]
    assert (blank["lesson_id"], blank["hint_ar"]) == (by_lesson["hiwar"], "تحية")
    assert (synonym["lesson_id"], synonym["hint_ar"]) == (by_lesson["nahw"], "مترادف")
    assert order["question_ar"] == f"{seed_tool.sets.WORD_ORDER_PREFIX}: خالد / اسمي"


async def test_replace_rebuilds_content_and_clears_activity_but_keeps_accounts(client, register, content):
    student = await register()
    await client.post(f"/api/me/srs/add-unit/{content.unit_a}", headers=student.headers)
    await client.post("/api/exercises/submit", headers=student.headers,
                      json={"exercise_id": content.ex_choice, "student_answer": "kitap"})

    await seed_tool.seed(replace=True, units=TINY_UNITS, unit_exercises={}, log=_quiet)

    assert await _count(models.Student) == 1
    assert (await _count(models.SRSCard), await _count(models.ExerciseAnswer)) == (0, 0)
    assert [u["unit_number"] for u in (await client.get("/api/units")).json()] == [1, 9]
    assert (await client.get("/api/me/progress", headers=student.headers)).status_code == 200


async def test_a_failed_seed_changes_nothing(content):
    broken = [dict(TINY_UNITS[0]), {"number": 2, "title_ar": "ناقصة"}]   # second unit lacks fields
    with pytest.raises(KeyError):
        await seed_tool.seed(replace=True, units=broken, log=_quiet)
    assert await _count(models.Unit) == 2
    assert await _count(models.Exercise) == 6      # the fixture content is still there


async def test_supplements_fill_the_grammar_lesson_and_can_be_repeated(client):
    await _empty_content()
    await seed_tool.seed(units=TINY_UNITS, unit_exercises=TINY_EXERCISES, with_supplements=True,
                         rng=random.Random(2), log=_quiet)
    units = (await client.get("/api/units")).json()

    async def grammar_lesson_exercises(unit):
        lessons = (await client.get(f"/api/units/{unit['id']}/lessons")).json()
        nahw = next(item["id"] for item in lessons if item["lesson_type"] == "nahw")
        everything = (await client.get(f"/api/units/{unit['id']}/exercises")).json()
        return [e for e in everything if e["lesson_id"] == nahw]

    # Unit 1: the grammar set replaces the lesson (the base synonym is gone), plus enrichment.
    unit_1 = await grammar_lesson_exercises(units[0])
    numbers = sorted(e["exercise_number"] for e in unit_1)
    assert numbers == list(range(1, 21)) + list(range(801, 821))
    assert {e["exercise_type"] for e in unit_1 if e["exercise_number"] > 800} == {
        "antonym", "plural", "synonym", "comprehension"}
    true_false = next(e for e in unit_1 if e["exercise_type"] == "true_false")
    assert true_false["correct_answer"] in ("صَحِيح", "خَطَأ")

    # Unit 9: word order 501+, match 601+, fill/translate 701+, enrichment 801+.
    unit_9 = await grammar_lesson_exercises(units[1])
    numbers = sorted(e["exercise_number"] for e in unit_9)
    assert numbers == (list(range(1, 6)) + list(range(501, 506)) + list(range(601, 606))
                       + list(range(701, 711)) + list(range(801, 821)))
    order = next(e for e in unit_9 if e["exercise_number"] == 501)
    assert order["question_ar"].startswith(seed_tool.sets.WORD_ORDER_PREFIX + ": ")
    match = next(e for e in unit_9 if e["exercise_number"] == 601)
    assert match["exercise_type"] == "match" and match["correct_answer"] in match["options"]
    translate = next(e for e in unit_9 if e["exercise_number"] == 706)
    assert translate["correct_answer"] == "kelime9-1"

    before = await _count(models.Exercise)
    await seed_tool.supplements_only(rng=random.Random(3), log=_quiet)
    assert await _count(models.Exercise) == before


async def test_rebuilding_supplements_will_not_silently_delete_answers(client, register):
    await _empty_content()
    await seed_tool.seed(units=TINY_UNITS, unit_exercises={}, with_supplements=True, log=_quiet)
    student = await register()
    unit = (await client.get("/api/units")).json()[1]
    exercise = next(e for e in (await client.get(f"/api/units/{unit['id']}/exercises")).json()
                    if e["exercise_number"] == 801)
    await client.post("/api/exercises/submit", headers=student.headers,
                      json={"exercise_id": exercise["id"], "student_answer": "x"})

    with pytest.raises(seed_tool.AnswersWouldBeDeletedError):
        await seed_tool.supplements_only(log=_quiet)
    assert await _count(models.ExerciseAnswer) == 1

    totals = await seed_tool.supplements_only(allow_deleting_answers=True, log=_quiet)
    assert totals["answers_deleted"] == 1 and await _count(models.ExerciseAnswer) == 0


async def test_book_3_units_hold_listening_texts_as_narration(client):
    await _empty_content()
    listening_unit = dict(TINY_UNITS[0], number=33, dialogues=[{
        "title": "نص مسموع", "speakers": [],
        "lines": [{"speaker": "", "text": "الفقرة الأولى."}, {"speaker": "", "text": "الفقرة الثانية."}]}])
    await seed_tool.seed(units=[TINY_UNITS[0], listening_unit], unit_exercises={},
                         rng=random.Random(1), log=_quiet)

    units = (await client.get("/api/units")).json()
    first_lessons = [(await client.get(f"/api/units/{u['id']}/lessons")).json()[0] for u in units]
    assert [(lesson["title_tr"], lesson["lesson_type"]) for lesson in first_lessons] == [
        ("Diyaloglar", "hiwar"), ("Dinleme Metinleri", "hiwar")]

    text = (await client.get(f"/api/lessons/{first_lessons[1]['id']}/dialogues")).json()[0]
    assert text["situation_tr"] == ""
    assert [(line["speaker"], line["text_ar"]) for line in text["lines"]] == [
        ("", "الفقرة الأولى."), ("", "الفقرة الثانية.")]
