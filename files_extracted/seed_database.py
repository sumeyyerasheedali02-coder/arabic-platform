from book1_part2_data import BOOK_1_PART_2
from book2_part1_data import BOOK_2_PART_1
from book2_part2_data import BOOK_2_PART_2
"""
Seed database with Book 1 Part 1 — 8 real units from العربية بين يديك.
Run once on a fresh database or to replace all content:
    python seed_database.py
Students are preserved; all content + progress tables are wiped and rebuilt.
"""
import asyncio
import sys
import os
import random
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from sqlalchemy import text, select
from exercises_data import EXERCISES_DATA
from database import (
    init_db, AsyncSessionLocal,
    Unit, Lesson, Vocabulary, Dialogue, DialogueLine, Exercise,
    SRSCard, Student, StudentProgress, ExerciseAnswer,
)

# Copy book data file into the backend directory if needed
"""
بيانات كتاب العربية بين يديك — الكتاب الأول الجزء الأول
مستخرجة من الكتاب الأصلي — 8 وحدات، 9 دروس لكل وحدة
"""

BOOK_1_PART_1 = {
    "id": 1,
    "title": "الكتاب الأول — الجزء الأول",
    "total_units": 8,
    "total_lessons": 72,
    "units": [

        # ═══════════════════════════════════════
        # الوحدة الأولى: التَّحِيَّة والتَّعَارُف
        # الدروس 1-9 | الصفحات 1-26
        # ═══════════════════════════════════════
        {
            "id": 1,
            "number": 1,
            "title_ar": "التَّحِيَّة والتَّعَارُف",
            "title_tr": "Selamlama ve Tanışma",
            "pages": "1-26",
            "color": "#1D9E75",
            "main_topics": [
                "إلقاء التحية",
                "التعريف بالنفس",
                "التعريف بالآخرين",
                "السؤال عن البلد والجنسية",
                "أسماء الإشارة: هَذَا / هَذِه",
                "أدوات الاستفهام: مَن / مِن أَيْن / هَل / مَا",
            ],
            "grammar": [
                "الاستفهام بـ: مَن / مِن أَيْن / هَل / مَا",
                "أسماء الإشارة: هَذَا — هَذِه",
                "الجنسية والنسبة",
            ],
            "dialogues": [
                {
                    "id": 1,
                    "lesson": 1,
                    "title": "الحِوَارُ الأَوَّل (أ)",
                    "speakers": ["خالد", "خَليل"],
                    "lines": [
                        {"speaker": "خالد", "text": "السَّلَامُ عَلَيْكُم."},
                        {"speaker": "خَليل", "text": "وَعَلَيْكُمُ السَّلَام."},
                        {"speaker": "خالد", "text": "اسْمِي خالِد، مَا اسْمُكَ؟"},
                        {"speaker": "خَليل", "text": "اسْمِي خَليل."},
                        {"speaker": "خالد", "text": "كَيْفَ حالُكَ؟"},
                        {"speaker": "خَليل", "text": "بِخَيْر، وَالحَمْدُ لله. وَكَيْفَ حالُكَ أَنْتَ؟"},
                        {"speaker": "خالد", "text": "بِخَيْر، وَالحَمْدُ لله."},
                    ]
                },
                {
                    "id": 2,
                    "lesson": 1,
                    "title": "الحِوَارُ الأَوَّل (ب)",
                    "speakers": ["خَوْلَة", "خَدِيجَة"],
                    "lines": [
                        {"speaker": "خَوْلَة", "text": "السَّلَامُ عَلَيْكُم."},
                        {"speaker": "خَدِيجَة", "text": "وَعَلَيْكُمُ السَّلَام."},
                        {"speaker": "خَوْلَة", "text": "اسْمِي خَوْلَة، مَا اسْمُكِ؟"},
                        {"speaker": "خَدِيجَة", "text": "اسْمِي خَدِيجَة."},
                        {"speaker": "خَوْلَة", "text": "كَيْفَ حالُكِ؟"},
                        {"speaker": "خَدِيجَة", "text": "بِخَيْر، وَالحَمْدُ لله. وَكَيْفَ حالُكِ أَنْتِ؟"},
                        {"speaker": "خَوْلَة", "text": "بِخَيْر، وَالحَمْدُ لله."},
                    ]
                },
                {
                    "id": 3,
                    "lesson": 4,
                    "title": "الحِوَارُ الثَّاني",
                    "speakers": ["غانِم", "طالِب"],
                    "lines": [
                        {"speaker": "غانِم", "text": "السَّلَامُ عَلَيْكُم."},
                        {"speaker": "طالِب", "text": "وَعَلَيْكُمُ السَّلَام."},
                        {"speaker": "غانِم", "text": "مِنْ أَيْنَ أَنْتَ؟"},
                        {"speaker": "طالِب", "text": "أَنَا مِنْ تُرْكِيَا. وَأَنْتَ؟"},
                        {"speaker": "غانِم", "text": "أَنَا مِنَ الكُوَيْت."},
                        {"speaker": "طالِب", "text": "مَا جِنْسِيَّتُكَ؟"},
                        {"speaker": "غانِم", "text": "أَنَا كُوَيْتِيٌّ."},
                    ]
                },
                {
                    "id": 4,
                    "lesson": 7,
                    "title": "الحِوَارُ الثَّالِث",
                    "speakers": ["أُسْتَاذ", "طَالِب"],
                    "lines": [
                        {"speaker": "أُسْتَاذ", "text": "مَنْ هَذَا؟"},
                        {"speaker": "طَالِب", "text": "هَذَا خَالِد."},
                        {"speaker": "أُسْتَاذ", "text": "مِنْ أَيْنَ هُوَ؟"},
                        {"speaker": "طَالِب", "text": "هُوَ مِنَ السُّعُودِيَّة."},
                        {"speaker": "أُسْتَاذ", "text": "وَمَنْ هَذِهِ؟"},
                        {"speaker": "طَالِب", "text": "هَذِهِ فَاطِمَة."},
                        {"speaker": "أُسْتَاذ", "text": "مِنْ أَيْنَ هِيَ؟"},
                        {"speaker": "طَالِب", "text": "هِيَ مِنَ الأُرْدُن."},
                    ]
                },
            ],
            "vocabulary": [
                {"word_ar": "السَّلَامُ عَلَيْكُم", "word_tr": "Selâmün aleyküm", "word_en": "Peace be upon you"},
                {"word_ar": "وَعَلَيْكُمُ السَّلَام", "word_tr": "Ve aleyküm selâm", "word_en": "And upon you peace"},
                {"word_ar": "اسْمِي", "word_tr": "benim adım", "word_en": "my name is"},
                {"word_ar": "مَا اسْمُكَ؟", "word_tr": "adın ne?", "word_en": "what is your name?"},
                {"word_ar": "كَيْفَ حَالُكَ؟", "word_tr": "nasılsın?", "word_en": "how are you?"},
                {"word_ar": "بِخَيْر", "word_tr": "iyiyim", "word_en": "fine"},
                {"word_ar": "وَالحَمْدُ لله", "word_tr": "Allah'a şükür", "word_en": "praise be to God"},
                {"word_ar": "مِنْ أَيْنَ أَنْتَ؟", "word_tr": "nerelisin?", "word_en": "where are you from?"},
                {"word_ar": "أَنَا مِن", "word_tr": "ben ... liyim", "word_en": "I am from"},
                {"word_ar": "هَذَا", "word_tr": "bu (eril)", "word_en": "this (masc.)"},
                {"word_ar": "هَذِهِ", "word_tr": "bu (dişil)", "word_en": "this (fem.)"},
                {"word_ar": "مَنْ؟", "word_tr": "kim?", "word_en": "who?"},
                {"word_ar": "هَل", "word_tr": "mı/mi?", "word_en": "is/are? (question)"},
                {"word_ar": "نَعَم", "word_tr": "evet", "word_en": "yes"},
                {"word_ar": "لَا", "word_tr": "hayır", "word_en": "no"},
                {"word_ar": "أَنْتَ", "word_tr": "sen (eril)", "word_en": "you (masc.)"},
                {"word_ar": "أَنْتِ", "word_tr": "sen (dişil)", "word_en": "you (fem.)"},
                {"word_ar": "هُوَ", "word_tr": "o (eril)", "word_en": "he"},
                {"word_ar": "هِيَ", "word_tr": "o (dişil)", "word_en": "she"},
                {"word_ar": "الجِنْسِيَّة", "word_tr": "milliyet", "word_en": "nationality"},
                # البلدان
                {"word_ar": "السُّعُودِيَّة", "word_tr": "Suudi Arabistan", "word_en": "Saudi Arabia"},
                {"word_ar": "تُرْكِيَا", "word_tr": "Türkiye", "word_en": "Turkey"},
                {"word_ar": "مِصْر", "word_tr": "Mısır", "word_en": "Egypt"},
                {"word_ar": "الأُرْدُن", "word_tr": "Ürdün", "word_en": "Jordan"},
                {"word_ar": "الكُوَيْت", "word_tr": "Kuveyt", "word_en": "Kuwait"},
                # الأعداد 1-5
                {"word_ar": "وَاحِد", "word_tr": "bir", "word_en": "one"},
                {"word_ar": "اثْنَان", "word_tr": "iki", "word_en": "two"},
                {"word_ar": "ثَلَاثَة", "word_tr": "üç", "word_en": "three"},
                {"word_ar": "أَرْبَعَة", "word_tr": "dört", "word_en": "four"},
                {"word_ar": "خَمْسَة", "word_tr": "beş", "word_en": "five"},
            ],
        },

        # ═══════════════════════════════════════
        # الوحدة الثانية: الأُسْرَة
        # الدروس 10-18 | الصفحات 27-51
        # ═══════════════════════════════════════
        {
            "id": 2,
            "number": 2,
            "title_ar": "الأُسْرَة",
            "title_tr": "Aile",
            "pages": "27-51",
            "color": "#185FA5",
            "main_topics": [
                "التعريف بأفراد الأسرة وأعمالهم",
                "الاستفسار عن أفراد الأسرة",
                "الاستفهام بـ: مَن / هَذَا / هَذِهِ — أَيْن",
                "الاستفهام عن الأفراد والأشياء",
            ],
            "grammar": [
                "الاستفهام بـ: مَن / هَذَا / هَذِه / أَيْن",
                "الضمائر المنفصلة",
                "المذكر والمؤنث",
            ],
            "dialogues": [
                {
                    "id": 1,
                    "lesson": 10,
                    "title": "الحِوَارُ الأَوَّل",
                    "speakers": ["سَامِي", "خَالِد"],
                    "lines": [
                        {"speaker": "سَامِي", "text": "هَلْ هَذِهِ أُسْرَتُكَ؟"},
                        {"speaker": "خَالِد", "text": "نَعَم، هَذِهِ أُسْرَتِي."},
                        {"speaker": "سَامِي", "text": "مَنْ هَذَا؟"},
                        {"speaker": "خَالِد", "text": "هَذَا أَبِي."},
                        {"speaker": "سَامِي", "text": "وَمَنْ هَذِهِ؟"},
                        {"speaker": "خَالِد", "text": "هَذِهِ أُمِّي."},
                        {"speaker": "سَامِي", "text": "وَهَذَا؟"},
                        {"speaker": "خَالِد", "text": "هَذَا أَخِي سَعِيد."},
                        {"speaker": "سَامِي", "text": "وَهَذِهِ؟"},
                        {"speaker": "خَالِد", "text": "هَذِهِ أُخْتِي نُورَة."},
                    ]
                },
                {
                    "id": 2,
                    "lesson": 11,
                    "title": "الحِوَارُ الثَّاني — أُسْرَة الرَّسُول ﷺ",
                    "speakers": ["عُمَر", "عُثْمَان"],
                    "lines": [
                        {"speaker": "عُمَر", "text": "هَلْ هَذِهِ شَجَرَة؟"},
                        {"speaker": "عُثْمَان", "text": "نَعَم، هَذِهِ أُسْرَةُ الرَّسُولِ صَلَّى اللهُ عَلَيْهِ وَسَلَّم."},
                        {"speaker": "عُمَر", "text": "هَذَا وَالِدُهُ عَبْدُ الله."},
                        {"speaker": "عُثْمَان", "text": "وَهَذِهِ وَالِدَتُهُ آمِنَة."},
                        {"speaker": "عُمَر", "text": "وَهَذَا جَدُّهُ عَبْدُ المُطَّلِب."},
                        {"speaker": "عُثْمَان", "text": "وَهَذَا عَمُّهُ العَبَّاس."},
                        {"speaker": "عُمَر", "text": "وَهَذَا ابْنُهُ القَاسِم."},
                        {"speaker": "عُثْمَان", "text": "وَهَذِهِ ابْنَتُهُ فَاطِمَة."},
                    ]
                },
                {
                    "id": 3,
                    "lesson": 14,
                    "title": "الحِوَارُ الثَّالِث",
                    "speakers": ["رَنَا", "سَلْوَى"],
                    "lines": [
                        {"speaker": "رَنَا", "text": "كَمْ أَخًا لَكِ؟"},
                        {"speaker": "سَلْوَى", "text": "لِي أَخَوَان."},
                        {"speaker": "رَنَا", "text": "وَكَمْ أُخْتًا لَكِ؟"},
                        {"speaker": "سَلْوَى", "text": "لِي ثَلَاثُ أَخَوَات."},
                        {"speaker": "رَنَا", "text": "أَيْنَ يَسْكُنُ أَبُوكِ؟"},
                        {"speaker": "سَلْوَى", "text": "يَسْكُنُ فِي الرِّيَاض."},
                    ]
                },
            ],
            "vocabulary": [
                {"word_ar": "الأُسْرَة", "word_tr": "aile", "word_en": "family"},
                {"word_ar": "الأَب", "word_tr": "baba", "word_en": "father"},
                {"word_ar": "الأُم", "word_tr": "anne", "word_en": "mother"},
                {"word_ar": "الأَخ", "word_tr": "erkek kardeş", "word_en": "brother"},
                {"word_ar": "الأُخْت", "word_tr": "kız kardeş", "word_en": "sister"},
                {"word_ar": "الجَدّ", "word_tr": "dede", "word_en": "grandfather"},
                {"word_ar": "الجَدَّة", "word_tr": "büyükanne", "word_en": "grandmother"},
                {"word_ar": "العَمّ", "word_tr": "amca", "word_en": "paternal uncle"},
                {"word_ar": "العَمَّة", "word_tr": "hala", "word_en": "paternal aunt"},
                {"word_ar": "الخَال", "word_tr": "dayı", "word_en": "maternal uncle"},
                {"word_ar": "الخَالَة", "word_tr": "teyze", "word_en": "maternal aunt"},
                {"word_ar": "الاِبْن", "word_tr": "oğul", "word_en": "son"},
                {"word_ar": "الاِبْنَة", "word_tr": "kız", "word_en": "daughter"},
                {"word_ar": "الزَّوْج", "word_tr": "koca/eş", "word_en": "husband"},
                {"word_ar": "الزَّوْجَة", "word_tr": "eş/hanım", "word_en": "wife"},
                # أماكن في البيت
                {"word_ar": "البَيْت", "word_tr": "ev", "word_en": "house"},
                {"word_ar": "الغُرْفَة", "word_tr": "oda", "word_en": "room"},
                {"word_ar": "المَطْبَخ", "word_tr": "mutfak", "word_en": "kitchen"},
                {"word_ar": "الحَمَّام", "word_tr": "banyo", "word_en": "bathroom"},
                {"word_ar": "غُرْفَةُ الجُلُوس", "word_tr": "oturma odası", "word_en": "living room"},
                # الأعداد 6-10
                {"word_ar": "سِتَّة", "word_tr": "altı", "word_en": "six"},
                {"word_ar": "سَبْعَة", "word_tr": "yedi", "word_en": "seven"},
                {"word_ar": "ثَمَانِيَة", "word_tr": "sekiz", "word_en": "eight"},
                {"word_ar": "تِسْعَة", "word_tr": "dokuz", "word_en": "nine"},
                {"word_ar": "عَشَرَة", "word_tr": "on", "word_en": "ten"},
            ],
        },

        # ═══════════════════════════════════════
        # الوحدة الثالثة: السَّكَن
        # الدروس 19-27 | الصفحات 52-79
        # ═══════════════════════════════════════
        {
            "id": 3,
            "number": 3,
            "title_ar": "السَّكَن",
            "title_tr": "Konut / Ev",
            "pages": "52-79",
            "color": "#854F0B",
            "main_topics": [
                "البحث عن سكن",
                "الاستفسار عن السكن: مكانه ونوعه ورقمه",
                "وصف البيت وغرفه",
                "أيام الأسبوع",
                "الاستفهام بـ: كَمْ + فعل مضارع / ماذا + فعل مضارع / كَمْ",
            ],
            "grammar": [
                "الاستفهام بـ: ماذا / كَم",
                "الفعل المضارع",
                "الأعداد الترتيبية",
            ],
            "dialogues": [
                {
                    "id": 1,
                    "lesson": 19,
                    "title": "الحِوَارُ الأَوَّل",
                    "speakers": ["طَالِب", "صَاحِبُ البَيْت"],
                    "lines": [
                        {"speaker": "طَالِب", "text": "السَّلَامُ عَلَيْكُم."},
                        {"speaker": "صَاحِبُ البَيْت", "text": "وَعَلَيْكُمُ السَّلَام."},
                        {"speaker": "طَالِب", "text": "هَلْ عِنْدَكَ غُرْفَة لِلإِيجَار؟"},
                        {"speaker": "صَاحِبُ البَيْت", "text": "نَعَم، عِنْدِي غُرْفَة."},
                        {"speaker": "طَالِب", "text": "فِي أَيِّ دَوْر؟"},
                        {"speaker": "صَاحِبُ البَيْت", "text": "فِي الدَّوْر الثَّاني."},
                        {"speaker": "طَالِب", "text": "كَمِ الإِيجَار؟"},
                        {"speaker": "صَاحِبُ البَيْت", "text": "الإِيجَار أَلْفُ رِيَال."},
                    ]
                },
                {
                    "id": 2,
                    "lesson": 20,
                    "title": "الحِوَارُ الثَّاني — إيجار شقة",
                    "speakers": ["المُسْتَأجِر", "المُؤَجِّر"],
                    "lines": [
                        {"speaker": "المُسْتَأجِر", "text": "السَّلَامُ عَلَيْكُم."},
                        {"speaker": "المُؤَجِّر", "text": "وَعَلَيْكُمُ السَّلَام."},
                        {"speaker": "المُسْتَأجِر", "text": "أُرِيدُ شَقَّةً مِنْ فَضْلِكَ."},
                        {"speaker": "المُؤَجِّر", "text": "لَدَيْنَا شَقَّة جَمِيلَة."},
                        {"speaker": "المُسْتَأجِر", "text": "كَمْ غُرْفَةً فِي الشَّقَّة؟"},
                        {"speaker": "المُؤَجِّر", "text": "فِي الشَّقَّة خَمْسُ غُرَف."},
                        {"speaker": "المُسْتَأجِر", "text": "فِي أَيِّ دَوْر الشَّقَّة؟"},
                        {"speaker": "المُؤَجِّر", "text": "الشَّقَّة فِي الدَّوْر الخَامِس."},
                        {"speaker": "المُسْتَأجِر", "text": "أُرِيدُ مُشَاهَدَة الشَّقَّة."},
                        {"speaker": "المُؤَجِّر", "text": "تَفَضَّل، ادْخُل، هَذَا بَابُ الشَّقَّة."},
                        {"speaker": "المُسْتَأجِر", "text": "هَذِهِ شَقَّة جَمِيلَة."},
                    ]
                },
            ],
            "vocabulary": [
                {"word_ar": "السَّكَن", "word_tr": "konut/ev", "word_en": "housing"},
                {"word_ar": "الشَّقَّة", "word_tr": "daire", "word_en": "apartment"},
                {"word_ar": "الغُرْفَة", "word_tr": "oda", "word_en": "room"},
                {"word_ar": "الإِيجَار", "word_tr": "kira", "word_en": "rent"},
                {"word_ar": "الدَّوْر", "word_tr": "kat", "word_en": "floor"},
                {"word_ar": "المُسْتَأجِر", "word_tr": "kiracı", "word_en": "tenant"},
                {"word_ar": "المُؤَجِّر", "word_tr": "kiraya veren", "word_en": "landlord"},
                {"word_ar": "جَمِيل / جَمِيلَة", "word_tr": "güzel", "word_en": "beautiful"},
                {"word_ar": "كَبِير / كَبِيرَة", "word_tr": "büyük", "word_en": "big"},
                {"word_ar": "صَغِير / صَغِيرَة", "word_tr": "küçük", "word_en": "small"},
                # الأثاث
                {"word_ar": "السَّرِير", "word_tr": "yatak", "word_en": "bed"},
                {"word_ar": "الطَّاوِلَة", "word_tr": "masa", "word_en": "table"},
                {"word_ar": "الكُرْسِي", "word_tr": "sandalye", "word_en": "chair"},
                {"word_ar": "الخِزَانَة", "word_tr": "dolap", "word_en": "wardrobe"},
                {"word_ar": "التِّلْفَاز", "word_tr": "televizyon", "word_en": "television"},
                # أيام الأسبوع
                {"word_ar": "الأَحَد", "word_tr": "Pazar", "word_en": "Sunday"},
                {"word_ar": "الاِثْنَيْن", "word_tr": "Pazartesi", "word_en": "Monday"},
                {"word_ar": "الثُّلَاثَاء", "word_tr": "Salı", "word_en": "Tuesday"},
                {"word_ar": "الأَرْبِعَاء", "word_tr": "Çarşamba", "word_en": "Wednesday"},
                {"word_ar": "الخَمِيس", "word_tr": "Perşembe", "word_en": "Thursday"},
                {"word_ar": "الجُمُعَة", "word_tr": "Cuma", "word_en": "Friday"},
                {"word_ar": "السَّبْت", "word_tr": "Cumartesi", "word_en": "Saturday"},
            ],
        },

        # ═══════════════════════════════════════
        # الوحدة الرابعة: الحَيَاة اليَوْمِيَّة
        # الدروس 28-36 | الصفحات 80-107
        # ═══════════════════════════════════════
        {
            "id": 4,
            "number": 4,
            "title_ar": "الحَيَاة اليَوْمِيَّة",
            "title_tr": "Günlük Hayat",
            "pages": "80-107",
            "color": "#712B13",
            "main_topics": [
                "السؤال عن الوقت",
                "وصف النشاط اليومي",
                "وسيلة المواصلات",
                "العطلة والأنشطة",
                "أدوات الاستفهام: مَتَى / أَيْن + فعل مضارع",
                "النفي بلا + فعل مضارع",
                "الاستقبال بـ: سـ",
            ],
            "grammar": [
                "الاستفهام بـ: مَتَى / أَيْن",
                "النفي بـ: لَا + فعل مضارع",
                "الاستقبال بـ: سَـ + فعل مضارع",
                "الأعداد الترتيبية للمذكر",
            ],
            "dialogues": [
                {
                    "id": 1,
                    "lesson": 28,
                    "title": "الحِوَارُ الأَوَّل",
                    "speakers": ["نَادِر", "سَالِم"],
                    "lines": [
                        {"speaker": "نَادِر", "text": "مَاذَا تَفْعَلُ صَبَاحًا؟"},
                        {"speaker": "سَالِم", "text": "أَسْتَيْقِظُ بَاكِرًا وَأُصَلِّي الفَجْر."},
                        {"speaker": "نَادِر", "text": "وَبَعْدَ الصَّلَاة؟"},
                        {"speaker": "سَالِم", "text": "أَتَنَاوَل الفُطُور ثُمَّ أَذْهَب إِلَى الجَامِعَة."},
                        {"speaker": "نَادِر", "text": "بِمَاذَا تَذْهَبُ؟"},
                        {"speaker": "سَالِم", "text": "أَذْهَب بِالسَّيَّارَة."},
                    ]
                },
                {
                    "id": 2,
                    "lesson": 30,
                    "title": "الحِوَارُ الثَّالِث",
                    "speakers": ["عَادِل", "فَيْصَل"],
                    "lines": [
                        {"speaker": "عَادِل", "text": "مَتَى تَسْتَيْقِظُ يَوْمَ العُطْلَة؟"},
                        {"speaker": "فَيْصَل", "text": "أَسْتَيْقِظُ مُبَكِّرًا."},
                        {"speaker": "عَادِل", "text": "وَمَتَى تَسْتَيْقِظُ أَنْتَ؟"},
                        {"speaker": "فَيْصَل", "text": "أَسْتَيْقِظُ مُتَأَخِّرًا."},
                        {"speaker": "فَيْصَل", "text": "مَاذَا تَفْعَلُ فِي الصَّبَاح؟"},
                        {"speaker": "عَادِل", "text": "أُشَاهِدُ التِّلْفَاز."},
                        {"speaker": "فَيْصَل", "text": "وَمَاذَا تَفْعَلُ أَنْتَ؟"},
                        {"speaker": "عَادِل", "text": "أَقْرَأُ صَحِيفَة أَوْ كِتَابًا."},
                        {"speaker": "فَيْصَل", "text": "أَيْنَ تُصَلِّي الجُمُعَة؟"},
                        {"speaker": "عَادِل", "text": "أُصَلِّي الجُمُعَة فِي المَسْجِد الكَبِير."},
                    ]
                },
            ],
            "vocabulary": [
                {"word_ar": "يَسْتَيْقِظُ", "word_tr": "uyanır", "word_en": "wakes up"},
                {"word_ar": "مُبَكِّرًا", "word_tr": "erken", "word_en": "early"},
                {"word_ar": "مُتَأَخِّرًا", "word_tr": "geç", "word_en": "late"},
                {"word_ar": "الفُطُور", "word_tr": "kahvaltı", "word_en": "breakfast"},
                {"word_ar": "الغَدَاء", "word_tr": "öğle yemeği", "word_en": "lunch"},
                {"word_ar": "العَشَاء", "word_tr": "akşam yemeği", "word_en": "dinner"},
                {"word_ar": "الصَّبَاح", "word_tr": "sabah", "word_en": "morning"},
                {"word_ar": "المَسَاء", "word_tr": "akşam", "word_en": "evening"},
                {"word_ar": "النَّهَار", "word_tr": "gündüz", "word_en": "daytime"},
                {"word_ar": "اللَّيْل", "word_tr": "gece", "word_en": "night"},
                {"word_ar": "العُطْلَة", "word_tr": "tatil", "word_en": "holiday/vacation"},
                {"word_ar": "يَذْهَبُ إِلَى", "word_tr": "...a gider", "word_en": "goes to"},
                {"word_ar": "يَقْرَأُ", "word_tr": "okur", "word_en": "reads"},
                {"word_ar": "يَكْتُبُ", "word_tr": "yazar", "word_en": "writes"},
                {"word_ar": "يُشَاهِدُ", "word_tr": "izler", "word_en": "watches"},
                {"word_ar": "التِّلْفَاز", "word_tr": "televizyon", "word_en": "television"},
                {"word_ar": "السَّيَّارَة", "word_tr": "araba", "word_en": "car"},
                {"word_ar": "الحَافِلَة", "word_tr": "otobüs", "word_en": "bus"},
                # الأعداد الترتيبية
                {"word_ar": "الأَوَّل", "word_tr": "birinci", "word_en": "first"},
                {"word_ar": "الثَّانِي", "word_tr": "ikinci", "word_en": "second"},
                {"word_ar": "الثَّالِث", "word_tr": "üçüncü", "word_en": "third"},
                {"word_ar": "الرَّابِع", "word_tr": "dördüncü", "word_en": "fourth"},
                {"word_ar": "الخَامِس", "word_tr": "beşinci", "word_en": "fifth"},
            ],
        },

        # ═══════════════════════════════════════
        # الوحدة الخامسة: الطَّعَام والشَّرَاب
        # الدروس 37-45 | الصفحات 108-134
        # ═══════════════════════════════════════
        {
            "id": 5,
            "number": 5,
            "title_ar": "الطَّعَام والشَّرَاب",
            "title_tr": "Yiyecek ve İçecek",
            "pages": "108-134",
            "color": "#3C3489",
            "main_topics": [
                "الاستفسار عن الوجبات ومكوناتها",
                "طلب الطعام والشراب",
                "التعبير عن الجوع والنهي",
                "الاستجابة بالنفي وبالإيجاب",
                "الفعل المضارع المؤنث",
                "التعجب بصيغة الاستفهام",
            ],
            "grammar": [
                "الاستجابة بـ: نَعَم / الفعل — الفعل المضارع لا + فعل مضارع",
                "التعجب: مَا هَذَا ؟!",
                "الفعل المضارع المسند للمؤنث (تَطْلُبِين، تَشْرَبِين)",
            ],
            "dialogues": [
                {
                    "id": 1,
                    "lesson": 37,
                    "title": "الحِوَارُ الأَوَّل",
                    "speakers": ["نَادِر", "نَادِيَة"],
                    "lines": [
                        {"speaker": "نَادِر", "text": "مَاذَا تَأْكُلِين؟"},
                        {"speaker": "نَادِيَة", "text": "آكُلُ سَمَكًا وَخُضَارًا."},
                        {"speaker": "نَادِر", "text": "وَمَاذَا تَشْرَبِين؟"},
                        {"speaker": "نَادِيَة", "text": "أَشْرَبُ عَصِيرًا."},
                        {"speaker": "نَادِر", "text": "هَلْ تُحِبِّين الشَّاي؟"},
                        {"speaker": "نَادِيَة", "text": "نَعَم، أُحِبُّ الشَّاي."},
                    ]
                },
                {
                    "id": 2,
                    "lesson": 39,
                    "title": "الحِوَارُ الثَّالِث",
                    "speakers": ["الزَّوْج", "الزَّوْجَة"],
                    "lines": [
                        {"speaker": "الزَّوْج", "text": "السَّلَامُ عَلَيْكُم."},
                        {"speaker": "الزَّوْجَة", "text": "وَعَلَيْكُمُ السَّلَام."},
                        {"speaker": "الزَّوْج", "text": "أَنَا جَوْعَان جِدًّا."},
                        {"speaker": "الزَّوْجَة", "text": "الغَدَاء عَلَى المَائِدَة."},
                        {"speaker": "الزَّوْج", "text": "مَا هَذَا؟! سَمَك وَلَحْم وَدَجَاج وَأُرُزٌّ وَسَلَطَة وَفَاكِهَة! هَذَا كَثِير جِدًّا."},
                        {"speaker": "الزَّوْجَة", "text": "لَا تَأْكُل... لَا تَأْكُل. اجْلِس."},
                        {"speaker": "الزَّوْج", "text": "لِمَاذَا؟ أَنَا جَوْعَان."},
                        {"speaker": "الزَّوْجَة", "text": "لَدَيْنَا ضُيُوف."},
                    ]
                },
            ],
            "vocabulary": [
                {"word_ar": "الطَّعَام", "word_tr": "yemek", "word_en": "food"},
                {"word_ar": "الشَّرَاب", "word_tr": "içecek", "word_en": "drink"},
                {"word_ar": "الخُبْز", "word_tr": "ekmek", "word_en": "bread"},
                {"word_ar": "الأُرُزّ", "word_tr": "pirinç", "word_en": "rice"},
                {"word_ar": "اللَّحْم", "word_tr": "et", "word_en": "meat"},
                {"word_ar": "الدَّجَاج", "word_tr": "tavuk", "word_en": "chicken"},
                {"word_ar": "السَّمَك", "word_tr": "balık", "word_en": "fish"},
                {"word_ar": "الخُضَار", "word_tr": "sebze", "word_en": "vegetables"},
                {"word_ar": "الفَاكِهَة", "word_tr": "meyve", "word_en": "fruit"},
                {"word_ar": "السَّلَطَة", "word_tr": "salata", "word_en": "salad"},
                {"word_ar": "الشَّاي", "word_tr": "çay", "word_en": "tea"},
                {"word_ar": "القَهْوَة", "word_tr": "kahve", "word_en": "coffee"},
                {"word_ar": "المَاء", "word_tr": "su", "word_en": "water"},
                {"word_ar": "العَصِير", "word_tr": "meyve suyu", "word_en": "juice"},
                {"word_ar": "الحَلِيب", "word_tr": "süt", "word_en": "milk"},
                {"word_ar": "جَوْعَان", "word_tr": "aç", "word_en": "hungry"},
                {"word_ar": "عَطْشَان", "word_tr": "susuz", "word_en": "thirsty"},
                {"word_ar": "لَذِيذ", "word_tr": "lezzetli", "word_en": "delicious"},
                {"word_ar": "الوَزْن", "word_tr": "ağırlık", "word_en": "weight"},
                {"word_ar": "الكِيلُو", "word_tr": "kilo", "word_en": "kilogram"},
            ],
        },

        # ═══════════════════════════════════════
        # الوحدة السادسة: الصَّلَاة
        # الدروس 46-54 | الصفحات 135-161
        # ═══════════════════════════════════════
        {
            "id": 6,
            "number": 6,
            "title_ar": "الصَّلَاة",
            "title_tr": "Namaz",
            "pages": "135-161",
            "color": "#1D9E75",
            "main_topics": [
                "التحدث عن الصلوات ومواقيتها وأماكنها",
                "الذهاب إلى المسجد",
                "الاعتذار بـ: آسف",
                "العطف بالواو",
                "الاستفهام بـ: لِمَاذَا + الفعل المضارع + الضمير ضَمِير الرَّفْع المُنْفَصِل",
                "فعل الأمر (أَنْتَ)",
            ],
            "grammar": [
                "العطف بالواو",
                "الاستفهام بـ: لِمَاذَا",
                "فعل الأمر للمفرد المذكر",
                "الاسم المبتدأ والخبر",
            ],
            "dialogues": [
                {
                    "id": 1,
                    "lesson": 46,
                    "title": "الحِوَارُ الأَوَّل",
                    "speakers": ["رَامِي", "سَعِيد"],
                    "lines": [
                        {"speaker": "رَامِي", "text": "مَتَى يَكُون أَذَان العَصْر؟"},
                        {"speaker": "سَعِيد", "text": "أَذَان العَصْر السَّاعَة الثَّالِثَة وَالنِّصْف."},
                        {"speaker": "رَامِي", "text": "أَيْن تُصَلِّي؟"},
                        {"speaker": "سَعِيد", "text": "أُصَلِّي فِي مَسْجِد الجَامِعَة."},
                        {"speaker": "رَامِي", "text": "هَلْ تَذْهَبُ الآن؟"},
                        {"speaker": "سَعِيد", "text": "نَعَم، تَعَال مَعِي."},
                        {"speaker": "رَامِي", "text": "آسِف، لَا أَسْتَطِيع الآن."},
                    ]
                },
                {
                    "id": 2,
                    "lesson": 48,
                    "title": "الحِوَارُ الثَّالِث",
                    "speakers": ["أَحْمَد", "مُحَمَّد"],
                    "lines": [
                        {"speaker": "أَحْمَد", "text": "كَمْ مَرَّة تُصَلِّي فِي اليَوْم؟"},
                        {"speaker": "مُحَمَّد", "text": "أُصَلِّي خَمْسَ مَرَّات."},
                        {"speaker": "أَحْمَد", "text": "مَا أَسْمَاء الصَّلَوَات؟"},
                        {"speaker": "مُحَمَّد", "text": "الفَجْر وَالظُّهْر وَالعَصْر وَالمَغْرِب وَالعِشَاء."},
                        {"speaker": "أَحْمَد", "text": "أَيْن تُصَلِّي الجُمُعَة؟"},
                        {"speaker": "مُحَمَّد", "text": "أُصَلِّي الجُمُعَة فِي المَسْجِد."},
                    ]
                },
            ],
            "vocabulary": [
                {"word_ar": "الصَّلَاة", "word_tr": "namaz", "word_en": "prayer"},
                {"word_ar": "المَسْجِد", "word_tr": "cami", "word_en": "mosque"},
                {"word_ar": "الأَذَان", "word_tr": "ezan", "word_en": "call to prayer"},
                {"word_ar": "الإِمَام", "word_tr": "imam", "word_en": "imam"},
                {"word_ar": "الوُضُوء", "word_tr": "abdest", "word_en": "ablution"},
                {"word_ar": "الرَّكْعَة", "word_tr": "rekat", "word_en": "unit of prayer"},
                {"word_ar": "السُّجُود", "word_tr": "secde", "word_en": "prostration"},
                {"word_ar": "القِبْلَة", "word_tr": "kıble", "word_en": "direction of prayer"},
                # أسماء الصلوات
                {"word_ar": "الفَجْر", "word_tr": "sabah namazı", "word_en": "dawn prayer"},
                {"word_ar": "الظُّهْر", "word_tr": "öğle namazı", "word_en": "noon prayer"},
                {"word_ar": "العَصْر", "word_tr": "ikindi namazı", "word_en": "afternoon prayer"},
                {"word_ar": "المَغْرِب", "word_tr": "akşam namazı", "word_en": "sunset prayer"},
                {"word_ar": "العِشَاء", "word_tr": "yatsı namazı", "word_en": "night prayer"},
                {"word_ar": "الجُمُعَة", "word_tr": "cuma namazı", "word_en": "Friday prayer"},
                # أفعال
                {"word_ar": "يُصَلِّي", "word_tr": "namaz kılar", "word_en": "prays"},
                {"word_ar": "يَذْهَبُ", "word_tr": "gider", "word_en": "goes"},
                {"word_ar": "آسِف", "word_tr": "üzgünüm/özür", "word_en": "sorry"},
                {"word_ar": "لَا أَسْتَطِيع", "word_tr": "yapamam", "word_en": "I cannot"},
                # الأعداد الترتيبية من السادس للعاشر
                {"word_ar": "السَّادِس", "word_tr": "altıncı", "word_en": "sixth"},
                {"word_ar": "السَّابِع", "word_tr": "yedinci", "word_en": "seventh"},
                {"word_ar": "الثَّامِن", "word_tr": "sekizinci", "word_en": "eighth"},
                {"word_ar": "التَّاسِع", "word_tr": "dokuzuncu", "word_en": "ninth"},
                {"word_ar": "العَاشِر", "word_tr": "onuncu", "word_en": "tenth"},
            ],
        },

        # ═══════════════════════════════════════
        # الوحدة السابعة: الدِّرَاسَة
        # الدروس 55-63 | الصفحات 162-188
        # ═══════════════════════════════════════
        {
            "id": 7,
            "number": 7,
            "title_ar": "الدِّرَاسَة",
            "title_tr": "Eğitim / Okul",
            "pages": "162-188",
            "color": "#185FA5",
            "main_topics": [
                "التوجيهات لفعل الشيء",
                "طلب الشيء",
                "الاستفسار عن الدراسة والدراسة والعطلة",
                "التحدث عن المستقبل",
                "الأمر بـ: فعل الثلاثي الصحيح + المفعول به",
                "الخبر المقدم مع المبتدأ",
            ],
            "grammar": [
                "فعل الأمر الثلاثي الصحيح",
                "كَان + يَكُون",
                "سـ (للاستقبال)",
                "أَوْ (للتخيير)",
                "فِي أَيِّ...؟ — قَرِيب مِن / بَعِيد عَن",
                "الفعل الماضي المسند إلى تاء المتكلم",
            ],
            "dialogues": [
                {
                    "id": 1,
                    "lesson": 55,
                    "title": "الحِوَارُ الأَوَّل",
                    "speakers": ["غَالِب", "خَوْلَة"],
                    "lines": [
                        {"speaker": "غَالِب", "text": "مَاذَا تَدْرُسِين؟"},
                        {"speaker": "خَوْلَة", "text": "أَدْرُسُ اللُّغَة العَرَبِيَّة."},
                        {"speaker": "غَالِب", "text": "فِي أَيِّ جَامِعَة؟"},
                        {"speaker": "خَوْلَة", "text": "فِي جَامِعَة الإِمَام."},
                        {"speaker": "غَالِب", "text": "هَلِ الجَامِعَة قَرِيبَة مِن بَيْتِكِ؟"},
                        {"speaker": "خَوْلَة", "text": "لَا، هِيَ بَعِيدَة."},
                    ]
                },
                {
                    "id": 2,
                    "lesson": 57,
                    "title": "الحِوَارُ الثَّالِث",
                    "speakers": ["قَاسِم", "غَانِم"],
                    "lines": [
                        {"speaker": "قَاسِم", "text": "هَلِ الدِّرَاسَة صَعْبَة؟"},
                        {"speaker": "غَانِم", "text": "بَعْضُهَا صَعْب وَبَعْضُهَا سَهْل."},
                        {"speaker": "قَاسِم", "text": "مَتَى تَبْدَأُ الدِّرَاسَة؟"},
                        {"speaker": "غَانِم", "text": "تَبْدَأُ السَّاعَة الثَّامِنَة صَبَاحًا."},
                        {"speaker": "قَاسِم", "text": "وَمَتَى تَنْتَهِي؟"},
                        {"speaker": "غَانِم", "text": "تَنْتَهِي السَّاعَة الثَّانِيَة ظُهْرًا."},
                        {"speaker": "قَاسِم", "text": "مَتَى الامْتِحَان؟"},
                        {"speaker": "غَانِم", "text": "الامْتِحَان يَوْم الخَمِيس."},
                    ]
                },
            ],
            "vocabulary": [
                {"word_ar": "الدِّرَاسَة", "word_tr": "eğitim/okuma", "word_en": "study/education"},
                {"word_ar": "الجَامِعَة", "word_tr": "üniversite", "word_en": "university"},
                {"word_ar": "الكُلِّيَة", "word_tr": "fakülte", "word_en": "faculty/college"},
                {"word_ar": "الفَصْل", "word_tr": "sınıf", "word_en": "classroom"},
                {"word_ar": "المَكْتَبَة", "word_tr": "kütüphane", "word_en": "library"},
                {"word_ar": "المُخْتَبَر", "word_tr": "laboratuvar", "word_en": "laboratory"},
                {"word_ar": "الطَّالِب", "word_tr": "öğrenci (erkek)", "word_en": "student (male)"},
                {"word_ar": "الطَّالِبَة", "word_tr": "öğrenci (kız)", "word_en": "student (female)"},
                {"word_ar": "الأُسْتَاذ", "word_tr": "hoca/öğretmen", "word_en": "professor/teacher"},
                {"word_ar": "الكِتَاب", "word_tr": "kitap", "word_en": "book"},
                {"word_ar": "الدَّرْس", "word_tr": "ders", "word_en": "lesson"},
                {"word_ar": "الامْتِحَان", "word_tr": "sınav", "word_en": "exam"},
                {"word_ar": "الوَاجِب", "word_tr": "ödev", "word_en": "homework"},
                {"word_ar": "العُطْلَة", "word_tr": "tatil", "word_en": "vacation/holiday"},
                {"word_ar": "المَوَاد الدِّرَاسِيَّة", "word_tr": "dersler", "word_en": "subjects"},
                {"word_ar": "العُلُوم", "word_tr": "fen/bilim", "word_en": "science"},
                {"word_ar": "الرِّيَاضِيَّات", "word_tr": "matematik", "word_en": "mathematics"},
                {"word_ar": "التَّارِيخ", "word_tr": "tarih", "word_en": "history"},
                {"word_ar": "قَرِيب مِن", "word_tr": "...a yakın", "word_en": "close to"},
                {"word_ar": "بَعِيد عَن", "word_tr": "...dan uzak", "word_en": "far from"},
            ],
        },

        # ═══════════════════════════════════════
        # الوحدة الثامنة: العَمَل
        # الدروس 64-72 | الصفحات 189-222
        # ═══════════════════════════════════════
        {
            "id": 8,
            "number": 8,
            "title_ar": "العَمَل",
            "title_tr": "İş / Meslek",
            "pages": "189-222",
            "color": "#854F0B",
            "main_topics": [
                "التعريف بالمهنة",
                "السؤال عن مكان العمل وعدد ساعات العمل",
                "السؤال عن الوظائف في الاستفسار عن الأطفال",
                "هَلْ + فعل مضارع — أَيْضًا",
                "الاستفهام بـ: هَل + فعل مضارع + الخبر المقدم",
                "الفعل الماضي المسند إلى تاء المتكلم",
            ],
            "grammar": [
                "الاستفهام بـ: هَل + فعل مضارع",
                "الخبر المقدم: لِي + المفعول المقدم",
                "الفعل الماضي المسند إلى تاء المتكلم",
                "الحَرَكَات الثَّلاث والسُّكُون",
            ],
            "dialogues": [
                {
                    "id": 1,
                    "lesson": 64,
                    "title": "الحِوَارُ الأَوَّل",
                    "speakers": ["صَالِح", "إِلْهَام"],
                    "lines": [
                        {"speaker": "صَالِح", "text": "مَا عَمَلُكِ؟"},
                        {"speaker": "إِلْهَام", "text": "أَنَا مُعَلِّمَة. وَأَنْت؟"},
                        {"speaker": "صَالِح", "text": "أَنَا طَبِيب."},
                        {"speaker": "إِلْهَام", "text": "أَيْن تَعْمَل؟"},
                        {"speaker": "صَالِح", "text": "أَعْمَلُ فِي المُسْتَشْفَى."},
                        {"speaker": "إِلْهَام", "text": "كَمْ سَاعَة تَعْمَلُ يَوْمِيًّا؟"},
                        {"speaker": "صَالِح", "text": "أَعْمَلُ ثَمَانِي سَاعَات."},
                    ]
                },
                {
                    "id": 2,
                    "lesson": 65,
                    "title": "الحِوَارُ الثَّاني",
                    "speakers": ["زَيْنَب", "مَرْيَم"],
                    "lines": [
                        {"speaker": "مَرْيَم", "text": "أَنَا مُدَرِّسَة. مَا مِهْنَتُكِ؟"},
                        {"speaker": "زَيْنَب", "text": "أَنَا مُدَرِّسَة أَيْضًا."},
                        {"speaker": "مَرْيَم", "text": "فِي أَيِّ مَرْحَلَة تُدَرِّسِين؟"},
                        {"speaker": "زَيْنَب", "text": "أُدَرِّسُ فِي المَرْحَلَة الاِبْتِدَائِيَّة. وَفِي أَيِّ مَرْحَلَة تُدَرِّسِين أَنْتِ؟"},
                        {"speaker": "مَرْيَم", "text": "أُدَرِّسُ فِي المَرْحَلَة المُتَوَسِّطَة."},
                        {"speaker": "زَيْنَب", "text": "هَلْ لَكِ أَطْفَال؟"},
                        {"speaker": "مَرْيَم", "text": "نَعَم، لِي أَطْفَال."},
                        {"speaker": "زَيْنَب", "text": "كَمْ طِفْلًا لَكِ؟"},
                        {"speaker": "مَرْيَم", "text": "لِي خَمْسَة أَطْفَال."},
                    ]
                },
                {
                    "id": 3,
                    "lesson": 66,
                    "title": "الحِوَارُ الثَّالِث",
                    "speakers": ["مَرْيَم", "زَيْنَب"],
                    "lines": [
                        {"speaker": "زَيْنَب", "text": "هَلْ تُحِبِّين عَمَلَكِ؟"},
                        {"speaker": "مَرْيَم", "text": "نَعَم، أُحِبُّ عَمَلِي. وَأَنَا أُحِبُّ عَمَلِي أَيْضًا."},
                    ]
                },
            ],
            "vocabulary": [
                {"word_ar": "العَمَل", "word_tr": "iş/meslek", "word_en": "work/job"},
                {"word_ar": "المِهْنَة", "word_tr": "meslek", "word_en": "profession"},
                # المهن
                {"word_ar": "الطَّبِيب", "word_tr": "doktor (erkek)", "word_en": "doctor (male)"},
                {"word_ar": "الطَّبِيبَة", "word_tr": "doktor (kadın)", "word_en": "doctor (female)"},
                {"word_ar": "المُعَلِّم", "word_tr": "öğretmen (erkek)", "word_en": "teacher (male)"},
                {"word_ar": "المُعَلِّمَة", "word_tr": "öğretmen (kadın)", "word_en": "teacher (female)"},
                {"word_ar": "المُهَنْدِس", "word_tr": "mühendis", "word_en": "engineer"},
                {"word_ar": "المُمَرِّضَة", "word_tr": "hemşire", "word_en": "nurse"},
                {"word_ar": "المُحَاسِب", "word_tr": "muhasebeci", "word_en": "accountant"},
                {"word_ar": "الصَّيْدَلَانِي", "word_tr": "eczacı", "word_en": "pharmacist"},
                {"word_ar": "المَحَامِي", "word_tr": "avukat", "word_en": "lawyer"},
                # أماكن العمل
                {"word_ar": "المُسْتَشْفَى", "word_tr": "hastane", "word_en": "hospital"},
                {"word_ar": "المَدْرَسَة", "word_tr": "okul", "word_en": "school"},
                {"word_ar": "الشَّرِكَة", "word_tr": "şirket", "word_en": "company"},
                {"word_ar": "المَكْتَب", "word_tr": "büro/ofis", "word_en": "office"},
                {"word_ar": "الدُّكَّان", "word_tr": "dükkan", "word_en": "shop"},
                # الساعة والوقت
                {"word_ar": "السَّاعَة", "word_tr": "saat", "word_en": "hour/clock"},
                {"word_ar": "الدَّقِيقَة", "word_tr": "dakika", "word_en": "minute"},
                {"word_ar": "النِّصْف", "word_tr": "buçuk/yarım", "word_en": "half"},
                {"word_ar": "الرُّبْع", "word_tr": "çeyrek", "word_en": "quarter"},
                {"word_ar": "يَوْمِيًّا", "word_tr": "günlük/her gün", "word_en": "daily"},
            ],
        },
    ]
}


def get_unit(unit_id: int) -> dict:
    """إرجاع بيانات وحدة معينة"""
    for unit in BOOK_1_PART_1["units"]:
        if unit["id"] == unit_id:
            return unit
    return None


def get_vocabulary(unit_id: int) -> list:
    """إرجاع مفردات وحدة معينة"""
    unit = get_unit(unit_id)
    return unit["vocabulary"] if unit else []


def get_dialogues(unit_id: int) -> list:
    """إرجاع حوارات وحدة معينة"""
    unit = get_unit(unit_id)
    return unit["dialogues"] if unit else []


def get_all_units_summary() -> list:
    """إرجاع ملخص جميع الوحدات"""
    return [
        {
            "id": u["id"],
            "number": u["number"],
            "title_ar": u["title_ar"],
            "title_tr": u["title_tr"],
            "color": u["color"],
            "vocab_count": len(u["vocabulary"]),
            "dialogue_count": len(u["dialogues"]),
        }
        for u in BOOK_1_PART_1["units"]
    ]




async def seed():
    await init_db()
    async with AsyncSessionLocal() as db:

        # ── Wipe content + activity (keep student accounts) ───────────
        for table in [
            "srs_cards", "exercise_answers", "student_progress",
            "exercises", "dialogue_lines", "dialogues",
            "vocabulary", "lessons", "units",
        ]:
            await db.execute(text(f"DELETE FROM {table}"))
        await db.commit()
        print("Cleared existing content.")

        # ── Fetch existing students for SRS card creation ──────────────
        result = await db.execute(select(Student))
        students = result.scalars().all()
        print(f"Found {len(students)} existing student(s).")

        all_vocab_ids = []

        # Renumber units across books
        b1p1 = BOOK_1_PART_1["units"]
        b1p2 = BOOK_1_PART_2["units"]
        b2p1 = [dict(u, number=u["number"]+16) for u in BOOK_2_PART_1["units"]]
        b2p2 = BOOK_2_PART_2["units"]
        all_units = b1p1 + b1p2 + b2p1 + b2p2
        for u_data in all_units:
            grammar_text = " | ".join(u_data["grammar"])
            topics_text  = " | ".join(u_data["main_topics"])

            unit = Unit(
                unit_number    = u_data["number"],
                title_ar       = u_data["title_ar"],
                title_tr       = u_data["title_tr"],
                description_ar = topics_text,
                description_tr = u_data["title_tr"],
                total_lessons  = 3,
            )
            db.add(unit)
            await db.flush()
            print(f"\n  Unit {unit.unit_number}: {unit.title_ar}  (id={unit.id})")

            # ── 3 lessons per unit ─────────────────────────────────────
            lesson_hiwar = Lesson(
                unit_id       = unit.id,
                lesson_number = 1,
                title_ar      = "الحِوَارَات",
                title_tr      = "Diyaloglar",
                lesson_type   = "hiwar",
            )
            lesson_mufradat = Lesson(
                unit_id       = unit.id,
                lesson_number = 2,
                title_ar      = "المُفْرَدَات",
                title_tr      = "Kelimeler",
                lesson_type   = "mufradat",
            )
            lesson_nahw = Lesson(
                unit_id       = unit.id,
                lesson_number = 3,
                title_ar      = "النَّحْو وَالتَّرَاكِيب",
                title_tr      = "Dilbilgisi",
                lesson_type   = "nahw",
                grammar_focus = grammar_text,
            )
            db.add_all([lesson_hiwar, lesson_mufradat, lesson_nahw])
            await db.flush()

            # ── Dialogues ─────────────────────────────────────────────
            for i, d in enumerate(u_data["dialogues"]):
                dialogue = Dialogue(
                    lesson_id       = lesson_hiwar.id,
                    dialogue_number = i + 1,
                    title_ar        = d["title"],
                    situation_tr    = "، ".join(d["speakers"]),
                )
                db.add(dialogue)
                await db.flush()
                for j, line in enumerate(d["lines"]):
                    db.add(DialogueLine(
                        dialogue_id    = dialogue.id,
                        line_order     = j + 1,
                        speaker        = line["speaker"],
                        text_ar        = line["text"],
                        translation_tr = None,
                        is_key_phrase  = False,
                    ))
            await db.flush()
            print(f"    dialogues : {len(u_data['dialogues'])}")

            # ── Vocabulary ────────────────────────────────────────────
            vocab_list = u_data["vocabulary"]
            new_vocab_ids = []
            for v in vocab_list:
                vocab = Vocabulary(
                    unit_id        = unit.id,
                    lesson_id      = lesson_mufradat.id,
                    word_ar        = v["word_ar"],
                    translation_tr = v["word_tr"],
                    translation_en = v["word_en"],
                    difficulty     = 1,
                )
                db.add(vocab)
                await db.flush()
                new_vocab_ids.append(vocab.id)
            all_vocab_ids.extend(zip([unit.id] * len(new_vocab_ids), new_vocab_ids))
            print(f"    vocabulary: {len(vocab_list)} words")

            # ── Exercises (auto-generated from vocabulary) ────────────
            ex_num = 0
            for i, v in enumerate(vocab_list):
                others = [x["word_tr"] for x in vocab_list if x["word_tr"] != v["word_tr"]]
                wrong  = random.sample(others, min(3, len(others)))
                opts   = wrong + [v["word_tr"]]
                random.shuffle(opts)

                ex_num += 1
                db.add(Exercise(
                    unit_id         = unit.id,
                    lesson_id       = lesson_mufradat.id,
                    exercise_number = ex_num,
                    exercise_type   = "multiple_choice",
                    question_ar     = f"مَا مَعْنَى كَلِمَة: {v['word_ar']}؟",
                    correct_answer  = v["word_tr"],
                    options         = opts,
                    difficulty      = 1,
                    points          = 10,
                ))

                # true/false — alternate correct/wrong to keep balance
                if i % 2 == 0:
                    shown_tr   = v["word_tr"]
                    correct_tf = "صَحِيح"
                else:
                    other_list = [x["word_tr"] for x in vocab_list if x["word_tr"] != v["word_tr"]]
                    shown_tr   = random.choice(other_list) if other_list else v["word_tr"]
                    correct_tf = "خَطَأ"

                ex_num += 1
                db.add(Exercise(
                    unit_id         = unit.id,
                    lesson_id       = lesson_mufradat.id,
                    exercise_number = ex_num,
                    exercise_type   = "true_false",
                    question_ar     = f"هَلْ مَعْنَى «{v['word_ar']}» بِالتُّرْكِيَّة: «{shown_tr}»؟",
                    correct_answer  = correct_tf,
                    options         = ["صَحِيح", "خَطَأ"],
                    difficulty      = 1,
                    points          = 5,
                ))

            # fill_blank
            unit_ex = EXERCISES_DATA.get(u_data["number"], {})
            for ex in unit_ex.get("fill_blank", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_hiwar.id,
                    exercise_number=ex_num, exercise_type="fill_blank",
                    question_ar=ex["q"], correct_answer=ex["answer"],
                    hint_ar=ex.get("hint"), options=None, difficulty=2, points=10))
            # translate_ar_tr
            for ex in unit_ex.get("translate_ar_tr", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_mufradat.id,
                    exercise_number=ex_num, exercise_type="translate_ar_tr",
                    question_ar=f"ترجم إلى التركية: {ex['q']}",
                    correct_answer=ex["answer"], options=ex.get("options"), difficulty=2, points=10))
            # translate_tr_ar
            for ex in unit_ex.get("translate_tr_ar", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_mufradat.id,
                    exercise_number=ex_num, exercise_type="translate_tr_ar",
                    question_ar=f"ترجم إلى العربية: {ex['q']}",
                    correct_answer=ex["answer"], options=ex.get("options"), difficulty=2, points=10))
            # match
            for match_data in unit_ex.get("match", []):
                for pair in match_data["pairs"]:
                    others = [p["tr"] for p in match_data["pairs"] if p["tr"] != pair["tr"]]
                    import random as rnd
                    wrong = rnd.sample(others, min(3, len(others)))
                    opts = wrong + [pair["tr"]]
                    rnd.shuffle(opts)
                    ex_num += 1
                    db.add(Exercise(unit_id=unit.id, lesson_id=lesson_mufradat.id,
                        exercise_number=ex_num, exercise_type="match",
                        question_ar=f"صل: {pair['ar']}",
                        correct_answer=pair["tr"], options=opts, difficulty=1, points=5))
            # synonyms
            for ex in unit_ex.get("synonyms", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_nahw.id,
                    exercise_number=ex_num, exercise_type="multiple_choice",
                    question_ar=ex["q"], correct_answer=ex["answer"],
                    options=ex.get("options"), hint_ar="مترادف", difficulty=3, points=15))
            # antonyms
            for ex in unit_ex.get("antonyms", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_nahw.id,
                    exercise_number=ex_num, exercise_type="multiple_choice",
                    question_ar=ex["q"], correct_answer=ex["answer"],
                    options=ex.get("options"), hint_ar="ضد / متعاكس", difficulty=3, points=15))
            # word_order
            for ex in unit_ex.get("word_order", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_hiwar.id,
                    exercise_number=ex_num, exercise_type="fill_blank",
                    question_ar=f"رَتِّب الكلمات: {' / '.join(ex['words'])}",
                    correct_answer=ex["answer"], hint_ar=ex.get("hint"),
                    options=None, difficulty=3, points=15))
            # comprehension
            for ex in unit_ex.get("comprehension", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_hiwar.id,
                    exercise_number=ex_num, exercise_type="multiple_choice",
                    question_ar=ex["passage"] + "\n\n" + ex["q"],


                    correct_answer=ex["answer"], options=ex.get("options"),
                    hint_ar="استيعاب قرائي", difficulty=3, points=20))
            # plural
            for ex in unit_ex.get("plural", []):
                ex_num += 1
                db.add(Exercise(unit_id=unit.id, lesson_id=lesson_nahw.id,
                    exercise_number=ex_num, exercise_type="multiple_choice",
                    question_ar=ex["q"], correct_answer=ex["answer"],
                    options=ex.get("options"), hint_ar="جمع الكلمة", difficulty=3, points=15))

            await db.flush()
            print(f"    exercises : {ex_num}")

        # ── SRS cards for every student × every vocab word ─────────────
        today = date.today().isoformat()
        srs_count = 0
        for student in students:
            for _unit_id, vocab_id in all_vocab_ids:
                db.add(SRSCard(
                    student_id    = student.id,
                    vocabulary_id = vocab_id,
                    ease_factor   = 2.5,
                    interval_days = 1,
                    repetitions   = 0,
                    next_review   = today,
                ))
                srs_count += 1

        await db.flush()
        await db.commit()
        print(f"\n  SRS cards : {srs_count} ({len(students)} students × {len(all_vocab_ids)} words)")
        print("\nDone! Database seeded with Book 1 Part 1 (8 units).")


if __name__ == "__main__":
    asyncio.run(seed())
