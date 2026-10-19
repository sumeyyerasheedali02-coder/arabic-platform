"""Replacing dialogues on a database that students already use."""
import pytest
from sqlalchemy import func, select

from tools import seed as seed_tool
from tools import update_dialogues as tool

from ._app import AsyncSessionLocal, models


def _unit(number, *dialogues):
    return {"number": number, "dialogues": [
        {"title": title, "speakers": sorted({s for s, _ in lines} - {""}),
         "lines": [{"speaker": s, "text": t} for s, t in lines]}
        for title, lines in dialogues]}


NEW_UNITS = [
    _unit(1, ("الحوار الأول", [("أحمد", "السلام عليكم."), ("بدر", "وعليكم السلام.")]),
             ("الحوار الثاني", [("", "(يدخل المعلم)"), ("المعلم", "صباح الخير.")])),
    _unit(2, ("نص مسموع", [("", "فقرة أولى."), ("", "فقرة ثانية.")])),
]


def _noop(*args):
    pass


async def _snapshot():
    async with AsyncSessionLocal() as db:
        lessons = (await db.execute(select(models.Lesson.id, models.Lesson.title_tr)
                                    .order_by(models.Lesson.id))).all()
        dialogues = (await db.execute(select(func.count()).select_from(models.Dialogue))).scalar()
        lines = (await db.execute(select(func.count()).select_from(models.DialogueLine))).scalar()
        answers = (await db.execute(select(func.count()).select_from(models.ExerciseAnswer))).scalar()
        return lessons, dialogues, lines, answers


async def _dialogue_texts(client, lesson_id):
    return [(d["title_ar"], [(line["speaker"], line["text_ar"]) for line in d["lines"]])
            for d in (await client.get(f"/api/lessons/{lesson_id}/dialogues")).json()]


async def test_dry_run_changes_nothing(content):
    before = await _snapshot()
    totals = await tool.update_dialogues(units=NEW_UNITS, log=_noop)
    assert totals["units_changed"] == 2 and totals["dialogues_added"] == 3
    assert await _snapshot() == before


async def test_apply_replaces_dialogues_and_keeps_student_data(client, register, content, monkeypatch):
    student = await register()
    await client.post("/api/exercises/submit", headers=student.headers,
                      json={"exercise_id": content.ex_choice, "student_answer": "kitap"})
    await client.post("/api/me/progress/update", headers=student.headers,
                      params={"lesson_id": content.a_hiwar, "score": 10, "status": "completed"})
    monkeypatch.setattr(seed_tool, "LISTENING_TEXTS_FROM_UNIT", 2)   # unit 2 holds a text here
    lessons_before, _, _, answers_before = await _snapshot()

    totals = await tool.update_dialogues(units=NEW_UNITS, apply=True, log=_noop)
    assert totals == dict(units_changed=2, units_unchanged=0, dialogues_removed=1, dialogues_added=3,
                          lines_removed=2, lines_added=6, titles_changed=1)

    lessons_after, dialogues, lines, answers_after = await _snapshot()
    assert [lesson_id for lesson_id, _ in lessons_after] == [lesson_id for lesson_id, _ in lessons_before]
    assert (dialogues, lines, answers_after) == (3, 6, answers_before)
    assert await _dialogue_texts(client, content.a_hiwar) == [
        ("الحوار الأول", [("أحمد", "السلام عليكم."), ("بدر", "وعليكم السلام.")]),
        ("الحوار الثاني", [("", "(يدخل المعلم)"), ("المعلم", "صباح الخير.")])]
    unit_b_lessons = (await client.get(f"/api/units/{content.unit_b}/lessons")).json()
    assert unit_b_lessons[0]["title_tr"] == "Dinleme Metinleri"
    assert (await client.get("/api/me/progress", headers=student.headers)).json()[0]["score"] == 10

    again = await tool.update_dialogues(units=NEW_UNITS, apply=True, log=_noop)
    assert (again["units_changed"], again["units_unchanged"]) == (0, 2)


async def test_unknown_unit_stops_everything(content):
    before = await _snapshot()
    with pytest.raises(tool.UnmatchedContentError, match="unit 33"):
        await tool.update_dialogues(units=NEW_UNITS + [_unit(33)], apply=True, log=_noop)
    assert await _snapshot() == before
