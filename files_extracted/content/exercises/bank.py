"""The balanced exercise bank: the same number of exercises of every kind in every unit.

Hand-written per unit (content/exercises/bank_book*.py), ten of each:

    synonym / antonym / plural   "word = answer"              ما مرادف «word»؟
    comprehension                "question = answer"          about the unit's dialogues/texts
    fill_blank                   "sentence ـــــ = answer = Turkish hint"
    word_order                   "w1 / w2 / w3 = sentence"    the words of the sentence, shuffled

Generated from the unit's vocabulary (content/books), ten of each:
translation (five each way) and matching (Arabic word -> Turkish meaning, four
options). Also generated: up to ten multiple-choice and ten true/false
questions that top those kinds up to twenty where a unit has fewer.

An answer may list accepted alternatives separated by " / " (see
app/services/answers.py); for one-word synonym/antonym/plural answers the form
with or without the article is accepted as well.

Exercise numbers identify bank rows in a database (tools.balance_exercises):
1101-1110 synonym, 1201 antonym, 1301 plural, 1401 comprehension, 1501 fill,
1601 word order, 1701 translation, 1801 matching, 1901 extra multiple choice,
2001 extra true/false. Nothing else uses numbers from 1100 up.
"""
import random
import re
from collections import Counter

from app.services.answers import accepted_answers, normalize_answer
from content.labels import ANSWER_FALSE, ANSWER_TRUE, HINT_WORD_ORDER, WORD_ORDER_PREFIX

PER_KIND = 10
CHOICE_TARGET = 20          # multiple choice and true/false shown per unit
BLANK = "ـــــ"
FIRST_BANK_NUMBER = 1100

# kind -> (first exercise number, exercise_type, lesson, points)
KINDS = {
    "synonym":       (1101, "synonym", "nahw", 10),
    "antonym":       (1201, "antonym", "nahw", 10),
    "plural":        (1301, "plural", "nahw", 10),
    "comprehension": (1401, "comprehension", "hiwar", 10),
    "fill_blank":    (1501, "fill_blank", "nahw", 10),
    "word_order":    (1601, "fill_blank", "nahw", 15),
    "translation":   (1701, None, "mufradat", 10),
    "match":         (1801, "match", "mufradat", 5),
    "extra_choice":  (1901, "multiple_choice", "mufradat", 10),
    "extra_true_false": (2001, "true_false", "mufradat", 5),
}
WRITTEN_KINDS = ("synonym", "antonym", "plural", "comprehension", "fill_blank", "word_order")
QUESTION = {
    "synonym": "ما مُرادِفُ «{}»؟",
    "antonym": "ما ضِدُّ «{}»؟",
    "plural": "ما جَمْعُ «{}»؟",
}


# Existing multiple-choice / true-false questions (from the seed's exercise sets)
# that are wrong or ambiguous; tools.balance_exercises hides them.
REJECTED = {
    1: ["[اختبار] أيّ كلمة تعني «الجنسية»؟"],                 # the answer is the question's own word
    3: ["[اختبار] «الأحد» أول الأسبوع."],                     # differs between countries
    5: ["صيغة التعجب الصحيحة:",                               # «ما هذا!» is not the exclamation form
        "«لا تأكل» للنهي.",                                   # unvocalised, it can be negation
        "المضارع للمذكر من «شرب»:"],                         # «يشرب» (an option) is masculine too
    7: ["أداة السؤال عن الجامعة:",                            # not a grammatical notion
        "[اختبار] حرف التخيير:"],                             # repeats an earlier question
    9: ["ما جمع «قميص»؟"],                                     # «أقمصة» (an option) is correct too
    10: ["ماذا نأخذ عندما تمطر؟"],                            # «معطف» (an option) fits as well
}


# Vocabulary words whose Arabic spelling was corrected in content/books.
# The balance tool renames these in the database so that the meaning sync
# (which matches by exact word_ar) still works.
VOCABULARY_RENAMES = {
    # (unit, old_word_ar) -> new_word_ar
    (13, "المُفَقُودَات"): "المَفْقُودَات",
    (20, "عَشَرَة دَقَائِق"): "عَشْرُ دَقَائِق",
    (30, "مَلَايِيز"): "مَالِيزْيَا",
}


class BankError(ValueError):
    """The bank data breaks a rule; the message names the unit and the line."""


def _lines(text: str) -> list[str]:
    return [line.strip() for line in (text or "").strip().splitlines() if line.strip()]


def _with_article_variants(answer: str) -> str:
    """«الأب» also accepts «أب» for one-word answers (the article is never added)."""
    forms = [form.strip() for form in answer.split("/")]
    extra = []
    for form in forms:
        bare = re.sub("[\u064b-\u0652\u0670]", "", form)
        if " " not in form and bare.startswith("ال") and len(bare) > 3:
            extra.append(form[form.index("ل") + 1:].lstrip("\u0652"))
    return " / ".join(dict.fromkeys(forms + extra))


def _written(unit: int, kind: str, text: str) -> list[dict]:
    first, exercise_type, lesson, points = KINDS[kind]
    rows = []
    for index, line in enumerate(_lines(text)):
        parts = [part.strip() for part in line.split(" = ")]
        where = f"unit {unit} {kind} line {index + 1} «{line}»"
        if kind == "fill_blank":
            if len(parts) != 3:
                raise BankError(f"{where}: expected «sentence = answer = hint»")
            question, answer, hint = parts
            if BLANK not in question:
                raise BankError(f"{where}: the sentence has no blank «{BLANK}»")
        elif len(parts) != 2:
            raise BankError(f"{where}: expected «question = answer»")
        else:
            (question, answer), hint = parts, None
        if not answer or "?" in answer or not question:
            raise BankError(f"{where}: empty or unfinished")
        if kind in QUESTION:
            if normalize_answer(question) in accepted_answers(answer):
                raise BankError(f"{where}: the answer repeats the word")
            answer = _with_article_variants(answer)
            question = QUESTION[kind].format(question)
        elif kind == "word_order":
            words = [w.strip() for w in question.split("/")]
            for form in answer.split("/"):
                if Counter(normalize_answer(form).split()) != Counter(normalize_answer(" ".join(words)).split()):
                    raise BankError(f"{where}: «{form.strip()}» does not use exactly the given words")
            question, hint = f"{WORD_ORDER_PREFIX}: {' / '.join(words)}", HINT_WORD_ORDER
        rows.append(dict(exercise_number=first + index, exercise_type=exercise_type, lesson=lesson,
                         question_ar=question, correct_answer=answer, hint_ar=hint, options=None,
                         difficulty=2, points=points))
    if len(rows) != PER_KIND:
        raise BankError(f"unit {unit} {kind}: {len(rows)} exercises, expected {PER_KIND}")
    questions = Counter(normalize_answer(row["question_ar"]) for row in rows)
    repeated = [q for q, n in questions.items() if n > 1]
    if repeated:
        raise BankError(f"unit {unit} {kind}: repeated question {repeated}")
    return rows


def _usable_words(vocabulary: list[dict]) -> list[dict]:
    """Words whose Turkish meaning is a plain word and is not shared with another word."""
    plain = [w for w in vocabulary
             if not re.search(r"[()]|\.\.\.|…", w["word_tr"]) and w["word_tr"].strip()]
    meanings = Counter(m for w in plain for m in set(accepted_answers(w["word_tr"])))
    arabic = Counter(normalize_answer(w["word_ar"]) for w in plain)
    return [w for w in plain
            if all(meanings[m] == 1 for m in set(accepted_answers(w["word_tr"])))
            and arabic[normalize_answer(w["word_ar"])] == 1]


def _distinct(meaning: str, others: list[str]) -> list[str]:
    """Options that cannot also be right: no shared accepted form with the answer."""
    own = set(accepted_answers(meaning))
    return [o for o in others if not own & set(accepted_answers(o))]


def generated(unit: int, vocabulary: list[dict]) -> list[dict]:
    words = _usable_words(vocabulary)
    if len(words) < PER_KIND:
        raise BankError(f"unit {unit}: only {len(words)} usable vocabulary words, need {PER_KIND}")
    rng = random.Random(unit * 1009)
    rows = []

    first, _, lesson, points = KINDS["translation"]
    for index, word in enumerate(words[:PER_KIND]):
        if index % 2 == 0:
            rows.append(dict(exercise_type="translate_ar_tr", question_ar=f"ترجم إلى التركية: {word['word_ar']}",
                             correct_answer=word["word_tr"]))
        else:
            rows.append(dict(exercise_type="translate_tr_ar", question_ar=f"ترجم إلى العربية: {word['word_tr']}",
                             correct_answer=_with_article_variants(word["word_ar"])))
        rows[-1].update(exercise_number=first + index, lesson=lesson, hint_ar=None, options=None,
                        difficulty=2, points=points)

    def choice_rows(kind, make):
        first, exercise_type, lesson, points = KINDS[kind]
        chosen = words[-PER_KIND:] if kind == "match" else words[len(words) // 2:] + words[:len(words) // 2]
        for index, word in enumerate(chosen[:PER_KIND]):
            row = make(word)
            row.update(exercise_number=first + index, exercise_type=exercise_type, lesson=lesson,
                       hint_ar=None, difficulty=1, points=points)
            rows.append(row)

    def match(word):
        others = _distinct(word["word_tr"], [w["word_tr"] for w in words if w is not word])
        options = rng.sample(others, 3) + [word["word_tr"]]
        rng.shuffle(options)
        return dict(question_ar=f"صل: {word['word_ar']}", correct_answer=word["word_tr"], options=options)

    def choice(word):
        others = [w["word_ar"] for w in words if w is not word
                  and not set(accepted_answers(w["word_ar"])) & set(accepted_answers(word["word_ar"]))]
        options = rng.sample(others, 3) + [word["word_ar"]]
        rng.shuffle(options)
        return dict(question_ar=f"أَيُّ كَلِمَةٍ مَعْنَاهَا «{word['word_tr']}»؟",
                    correct_answer=word["word_ar"], options=options)

    def true_false(word):
        if rng.random() < 0.5:
            shown, answer = word["word_tr"], ANSWER_TRUE
        else:
            shown, answer = rng.choice(_distinct(word["word_tr"], [w["word_tr"] for w in words if w is not word])), ANSWER_FALSE
        return dict(question_ar=f"كَلِمَةُ «{word['word_ar']}» مَعْنَاهَا بِالتُّرْكِيَّة «{shown}».",
                    correct_answer=answer, options=[ANSWER_TRUE, ANSWER_FALSE])

    choice_rows("match", match)
    choice_rows("extra_choice", choice)
    choice_rows("extra_true_false", true_false)
    return rows


def unit_bank(unit: int, written: dict, vocabulary: list[dict]) -> list[dict]:
    """Every bank exercise of one unit; raises BankError on any rule broken."""
    rows = []
    for kind in WRITTEN_KINDS:
        rows += _written(unit, kind, written.get(kind, ""))
    rows += generated(unit, vocabulary)
    numbers = Counter(row["exercise_number"] for row in rows)
    if any(n > 1 for n in numbers.values()):
        raise BankError(f"unit {unit}: repeated exercise number")
    return rows


def full_bank(units=None) -> dict[int, list[dict]]:
    """unit number -> bank rows, for every unit of the course."""
    from content.books import all_units
    from content.exercises.bank_book1_part1 import BANK as B11
    from content.exercises.bank_book1_part2 import BANK as B12
    from content.exercises.bank_book2_part1 import BANK as B21
    from content.exercises.bank_book2_part2 import BANK as B22
    from content.exercises.bank_book3_part1 import BANK as B31
    from content.exercises.bank_book3_part2 import BANK as B32

    written = {**B11, **B12, **B21, **B22, **B31, **B32}
    units = all_units() if units is None else units
    return {u["number"]: unit_bank(u["number"], written[u["number"]], u["vocabulary"])
            for u in units if u["number"] in written}
