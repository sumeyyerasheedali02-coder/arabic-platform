"""Hand-written exercise sets, keyed by course unit number.

Base content (loaded by every seed):
    EXERCISES_DATA     units 1–8, mixed kinds

Supplementary sets (loaded only with `tools.seed --with-supplements`); they all
go into the unit's grammar lesson:
    GRAMMAR_EXERCISES  units 1–16  grammar questions + end-of-unit test
    WORD_ORDER         units 9–48  exercise numbers 501+
    FILL_BLANK         units 9–48  exercise numbers 701+
    ENRICHMENT         units 1–48  exercise numbers 801+
"""
from content.exercises.base_units_1_8 import EXERCISES_DATA
from content.exercises.enrichment_units_1_48 import ENRICHMENT
from content.exercises.fill_blank_units_9_48 import FILL_BLANK
from content.exercises.grammar_units_1_16 import GRAMMAR_EXERCISES
from content.exercises.word_order_units_9_48 import WORD_ORDER

# Fixed texts (hints, the word-order prefix, true/false answers) live in
# content/labels.py and are re-exported here for the seeding tool.
from content.labels import (  # noqa: E402
    ANSWER_FALSE,
    ANSWER_TRUE,
    HINT_ANTONYM,
    HINT_COMPREHENSION,
    HINT_FILL_BLANK,
    HINT_PLURAL,
    HINT_SYNONYM,
    HINT_TRANSLATE_TO_TURKISH,
    HINT_WORD_ORDER,
    WORD_ORDER_PREFIX,
)

__all__ = [
    "ANSWER_FALSE", "ANSWER_TRUE", "ENRICHMENT", "EXERCISES_DATA", "FILL_BLANK",
    "GRAMMAR_EXERCISES", "HINT_ANTONYM", "HINT_COMPREHENSION", "HINT_FILL_BLANK",
    "HINT_PLURAL", "HINT_SYNONYM", "HINT_TRANSLATE_TO_TURKISH", "HINT_WORD_ORDER",
    "WORD_ORDER", "WORD_ORDER_PREFIX",
]
