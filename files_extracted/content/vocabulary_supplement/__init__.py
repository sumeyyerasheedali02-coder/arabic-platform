"""Extra vocabulary taken from the course books' own unit word lists.

The base content (`content/books`) holds 998 words. The books list far more
words per unit than that; this package holds the ones missing, as plain data
(no database access). They are added to a database that already has content by
`app/services/vocabulary_supplement.py`, through migration 0010 and
`python -m tools.add_vocabulary`; `tools.seed` does not load them.

    SUPPLEMENT_VOCABULARY[unit_number] -> [{word_ar, word_tr, word_en}, ...]

Only course units 1-32 (books 1 and 2) are covered.
"""
from content.vocabulary_supplement import book1_part1, book1_part2, book2_part1, book2_part2

_PARTS = (book1_part1, book1_part2, book2_part1, book2_part2)


def _build() -> dict[int, list[dict]]:
    words: dict[int, list[dict]] = {}
    for part in _PARTS:
        for unit_number, rows in part.WORDS.items():
            if unit_number in words:
                raise ValueError(f"unit {unit_number} appears in two supplement files")
            words[unit_number] = [{"word_ar": ar, "word_tr": tr, "word_en": en} for ar, tr, en in rows]
    return dict(sorted(words.items()))


SUPPLEMENT_VOCABULARY: dict[int, list[dict]] = _build()

__all__ = ["SUPPLEMENT_VOCABULARY"]
