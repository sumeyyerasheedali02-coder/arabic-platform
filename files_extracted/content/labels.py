"""Fixed texts stored with exercises.

They are defined once here and used by name everywhere else (the seeding tool
writes them, the API derives each exercise's category from them). This module
holds no exercise data, so the running application can import it cheaply.
"""

# Hints that mark what an exercise practises.
HINT_SYNONYM = "مترادف"
HINT_ANTONYM = "ضد / متعاكس"
HINT_PLURAL = "جمع الكلمة"
HINT_COMPREHENSION = "استيعاب قرائي"
HINT_WORD_ORDER = "رتب الكلمات"
HINT_FILL_BLANK = "أكمل الفراغ"
HINT_TRANSLATE_TO_TURKISH = "ترجم للتركية"

# How a word-order question starts: «رَتِّب الكلمات: كلمة / كلمة / …».
# The first word is spelled out below because its shadda (U+0651) comes before
# its kasra (U+0650). The reverse order looks identical on screen but is a
# different string; exact-text matching on it broke the word-order filter for
# units 9–48 in the past. Nothing compares this text exactly any more (see
# app/services/exercise_categories.py), but new content should still use it.
WORD_ORDER_VERB = "".join(map(chr, (0x0631, 0x064E, 0x062A, 0x0651, 0x0650, 0x0628)))
WORD_ORDER_PREFIX = f"{WORD_ORDER_VERB} الكلمات"

# The two answers of a true/false exercise, exactly as the frontend sends them.
ANSWER_TRUE = "صَحِيح"
ANSWER_FALSE = "خَطَأ"
