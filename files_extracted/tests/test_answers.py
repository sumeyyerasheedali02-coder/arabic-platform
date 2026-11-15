import pytest

from app.services.answers import is_correct_answer, is_typed_exercise


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


@pytest.mark.parametrize("given,expected,correct", [
    # the alef after «ال» and its prefixes is a word-initial alef
    ("الاخت", "الأَخْت", True),
    ("والافطار", "وَالإِفْطَارُ", True),
    ("للام", "لِلْأُمِّ", True),
    # a final ة/ه and ى/ي are typed alike
    ("غرفه", "غُرْفَةِ", True),
    ("مستشفي", "مُسْتَشْفَى", True),
    ("هى", "هِيَ", True),
    ("الساعه الان", "السَّاعَةَ الآنَ", True),
    # inside a word they stay different letters: سال ≠ سأل, بدا ≠ بدأ
    ("سال", "سَأَلَ", False),
    ("بدا", "بَدَأَ", False),
    ("مكتبه", "مَكْتَبٌ", False),
])
def test_alef_after_the_article_and_final_endings(given, expected, correct):
    assert is_correct_answer(given, expected) is correct


@pytest.mark.parametrize("given,expected,typed,correct", [
    ("قلم", "القَلَمِ", True, True),
    ("القلم", "قَلَم", True, True),
    ("ام", "الأم", True, True),
    ("الام", "أم", True, True),
    ("قلم", "القَلَمِ", False, False),            # picking an option must not match its «ال» twin
    ("كتاب جميل", "الكتاب الجميل", True, False),     # a phrase keeps its article
    ("الأب", "الأم", True, False),
    ("ال", "الا", True, False),
])
def test_typed_answers_ignore_the_article_of_a_single_word(given, expected, typed, correct):
    assert is_correct_answer(given, expected, typed=typed) is correct


def test_which_exercises_are_typed():
    assert is_typed_exercise("fill_blank", None) and is_typed_exercise("synonym", [])
    assert is_typed_exercise("translate_ar_tr", None)
    assert not is_typed_exercise("multiple_choice", ["أ", "ب"])
    assert not is_typed_exercise("true_false", None) and not is_typed_exercise("match", ["a"])
    assert not is_typed_exercise("fill_blank", ["أ", "ب"])   # shown as buttons when it has options


@pytest.mark.parametrize("given,expected,typed,correct", [
    # ى typed for ي, and a missing madda, anywhere in the word
    ("علىكم", "عَلَيْكُم", False, True),
    ("مدىنه", "مَدِينَةٌ", False, True),
    ("مراه", "مِرْآة", False, True),
    # spaces and the kind of apostrophe do not matter in a typed answer
    ("و عليكم السلام", "وَعَلَيْكُمُ السَّلَام", True, True),
    ("الحمدلله", "الحَمْدُ لله", True, True),
    ("عبدالمطلب", "عَبْدُ المُطَّلِب", True, True),
    ("selamünaleyküm", "Selâmün aleyküm", True, True),
    ("büyük anne", "büyükanne", True, True),
    ("allah’a şükür", "Allah'a şükür", True, True),
    ("allaha şükür", "Allah'a şükür", True, True),
    ("و عليكم السلام", "وَعَلَيْكُمُ السَّلَام", False, False),
    # but the order of the words does, and so does a different word
    ("عليكم السلام", "وَعَلَيْكُمُ السَّلَام", True, False),
    ("السلام عليكم", "عليكم السلام", True, False),
    ("سال", "سَأَلَ", True, False),
    # the alef that carries a tanwin of fatha is optional in a typed answer
    ("مهندس", "مُهَنْدِسًا", True, True),
    ("مهندسا", "مُهَنْدِسًا", True, True),
    ("مهندس", "مُهَنْدِسًا", False, False),
    ("عصا", "عَصَا", True, True),
    ("عص", "عَصَا", True, False),
])
def test_typed_answers_tolerate_spacing_apostrophes_and_the_tanwin_alef(given, expected, typed, correct):
    assert is_correct_answer(given, expected, typed=typed) is correct
