"""Reviewed extra answers of the exercise bank (content/exercises/alternatives.py)."""
import pytest

from app.services.answers import is_correct_answer
from content.exercises.alternatives import ALTERNATIVES
from content.exercises.bank import BankError, apply_alternatives, full_bank


@pytest.fixture(scope="module")
def rows():
    return {(unit, row["exercise_number"]): row for unit, bank in full_bank().items() for row in bank}


def test_every_alternative_is_attached_to_its_exercise(rows):
    for (unit, number), (_guard, extra) in ALTERNATIVES.items():
        row = rows[(unit, number)]
        for form in extra.split(" / "):
            assert is_correct_answer(form, row["correct_answer"], typed=True), (unit, number, form)


@pytest.mark.parametrize("unit,number,typed_answer", [
    (12, 1707, "yolculuk"),            # السَّفَر
    (10, 1708, "حار"),                 # Sıcak
    (1, 1703, "ismim"),                # اسْمِي
    (1, 1707, "elhamdülillah"),
    (7, 1704, "الصف"),                 # sınıf
    (8, 1507, "كل يوم"),
    (10, 1310, "سحابات"),
])
def test_valid_answers_that_students_gave_are_accepted(rows, unit, number, typed_answer):
    assert is_correct_answer(typed_answer, rows[(unit, number)]["correct_answer"], typed=True)


@pytest.mark.parametrize("unit,number,typed_answer", [
    (12, 1707, "okul"),
    (10, 1708, "soğuk"),
    (1, 1707, "merhaba"),
    (7, 1704, "مدرسة"),
])
def test_wrong_answers_are_still_wrong(rows, unit, number, typed_answer):
    assert not is_correct_answer(typed_answer, rows[(unit, number)]["correct_answer"], typed=True)


def test_an_alternative_that_points_at_another_question_is_refused(rows, monkeypatch):
    monkeypatch.setattr("content.exercises.alternatives.ALTERNATIVES", {(12, 1707): ("سؤال آخر", "x")})
    with pytest.raises(BankError):
        apply_alternatives(12, [dict(row) for (unit, _), row in rows.items() if unit == 12])
