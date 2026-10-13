"""«العربية بين يديك»: three books, two parts each, eight units per part.

Every unit is a dict:
    number       unit number inside the course (1–48 after `all_units()`)
    title_ar / title_tr
    main_topics  list of topic titles          -> Unit.description_ar
    grammar      list of grammar points        -> grammar lesson (Lesson.grammar_focus)
    dialogues    [{title, speakers, lines: [{speaker, text}]}]
    vocabulary   [{word_ar, word_tr, word_en}]
"""
from content.books.book1_part1 import BOOK_1_PART_1
from content.books.book1_part2 import BOOK_1_PART_2
from content.books.book2_part1 import BOOK_2_PART_1
from content.books.book2_part2 import BOOK_2_PART_2
from content.books.book3_part1 import BOOK_3_PART_1
from content.books.book3_part2 import BOOK_3_PART_2

UNITS_PER_PART = 8

# (book part, offset added to its own unit numbers). Book 2 part 1 numbers its
# units 1–8 in the source file; in the course they are units 17–24.
_PARTS = (
    (BOOK_1_PART_1, 0),
    (BOOK_1_PART_2, 0),
    (BOOK_2_PART_1, 16),
    (BOOK_2_PART_2, 0),
    (BOOK_3_PART_1, 0),
    (BOOK_3_PART_2, 0),
)


def all_units() -> list[dict]:
    """All 48 units in course order, numbered 1–48."""
    units = [
        dict(unit, number=unit["number"] + offset)
        for part, offset in _PARTS
        for unit in part["units"]
    ]
    numbers = [unit["number"] for unit in units]
    if numbers != list(range(1, len(units) + 1)):
        raise ValueError(f"unit numbers are not consecutive: {numbers}")
    return units
