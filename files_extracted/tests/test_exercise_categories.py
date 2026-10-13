from app.services.exercise_categories import exercise_category
from content import labels

SHADDA, KASRA, FATHA = chr(0x0651), chr(0x0650), chr(0x064E)
SHADDA_FIRST = "ر" + FATHA + "ت" + SHADDA + KASRA + "ب"     # as the base content writes it
KASRA_FIRST = "ر" + FATHA + "ت" + KASRA + SHADDA + "ب"      # as two old scripts wrote it


def test_the_two_spellings_look_the_same_but_are_different_strings():
    assert SHADDA_FIRST != KASRA_FIRST
    assert labels.WORD_ORDER_VERB == SHADDA_FIRST


def test_word_order_is_recognised_whatever_the_diacritics():
    for verb in (SHADDA_FIRST, KASRA_FIRST, "رتب", "رَتِّبِ"):
        assert exercise_category("fill_blank", None, f"{verb} الكلمات: خالد / اسمي") == "word_order"
    assert exercise_category("fill_blank", "رتب الكلمات لتكوين جملة", "خالد / اسمي") == "word_order"
    assert exercise_category("fill_blank", "تحية", "السلام ___") is None


def test_hint_marks_the_category_of_multiple_choice_questions():
    assert exercise_category("multiple_choice", labels.HINT_SYNONYM, "س") == "synonym"
    assert exercise_category("multiple_choice", labels.HINT_ANTONYM, "س") == "antonym"
    assert exercise_category("multiple_choice", labels.HINT_PLURAL, "س") == "plural"
    assert exercise_category("multiple_choice", labels.HINT_COMPREHENSION, "س") == "comprehension"
    assert exercise_category("multiple_choice", None, "ما معنى كلمة: كتاب؟") is None


def test_supplementary_sets_carry_the_category_as_their_type():
    for kind in ("synonym", "antonym", "plural", "comprehension"):
        assert exercise_category(kind, "أي تلميح", "س") == kind


def test_missing_fields_are_tolerated():
    assert exercise_category(None, None, None) is None
