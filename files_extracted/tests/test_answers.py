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


@pytest.mark.parametrize("given,expected,correct", [
    ("من اين انت", "مِنْ أَيْنَ أَنْتَ؟", True),
    ("اسمي   خالد.", "اسمي خالد", True),
    ("«بيت»", "بيت", True),
    ("Köy", "Kırsal / Köy", True),
    ("kırsal", "Kırsal / Köy", True),
    ("Kırsal / Köy", "Kırsal / Köy", True),
    ("Şehir", "Kırsal / Köy", False),
    ("/", "Kırsal / Köy", False),
    ("", "بيت", False),
    ("kiz", "kız", True),
    ("İYİ", "iyi", True),
    ("KITAP", "kitap", True),
    ("بلى", "أَجَلْ / بَلَى", True),
    ("selamun aleykum", "Selâmün aleyküm", False),
    ("Selamün aleyküm", "Selâmün aleyküm", True),
])
def test_punctuation_alternatives_and_turkish_i(given, expected, correct):
    assert is_correct_answer(given, expected) is correct
