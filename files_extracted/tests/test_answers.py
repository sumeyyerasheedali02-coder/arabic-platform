import pytest

from app.services.answers import is_correct_answer


@pytest.mark.parametrize("given,expected,correct", [
    ("انا", "أَنَا", True),
    ("الى", "إِلَى", True),
    ("آنا", "أَنَا", True),
    ("ٱسم", "اسم", True),
    ("انا اذهب الى احمد", "أَنَا أَذْهَبُ إِلَى أَحْمَد", True),
    ("(الى) احمد", "(إِلَى) أَحْمَد", True),
    ("ا\u0655لى", "إِلَى", True),
    ("سا\u0654ل", "سَأَلَ", True),
    ("هذا", "هَٰذَا", True),
    ("سال", "سَأَلَ", False),
    ("بدا", "بَدَأَ", False),
    ("على", "إِلَى", False),
])
def test_forgiving_arabic_answer_check(given, expected, correct):
    assert is_correct_answer(given, expected) is correct
