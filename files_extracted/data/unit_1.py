"""
بيانات الوحدة الأولى: التحية والتعارف
مستخرجة من كتاب العربية بين يديك - الجزء الأول
"""

UNIT_1 = {
    "unit_number": 1,
    "title_ar": "التَّحِيَّةُ وَالتَّعَارُف",
    "title_tr": "Selamlama ve Tanışma",
    "description_ar": "تعلم كيفية التحية والتعارف باللغة العربية",
    "description_tr": "Arapça'da nasıl selaşılacağını ve tanışılacağını öğren",

    # ================================================================
    # المفردات الأساسية للوحدة الأولى
    # ================================================================
    "vocabulary": [
        # التحيات
        {"word_ar": "السَّلَامُ عَلَيْكُم",  "word_type": "تحية", "translation_tr": "Selam (İslami selamlama)",     "translation_en": "Peace be upon you",          "example_ar": "السَّلَامُ عَلَيْكُم يَا أَخِي",        "example_tr": "Selam olsun sana kardeşim"},
        {"word_ar": "وَعَلَيْكُمُ السَّلَام", "word_type": "تحية", "translation_tr": "Selamın üzerine olsun (cevap)", "translation_en": "And peace be upon you",       "example_ar": "وَعَلَيْكُمُ السَّلَام وَرَحْمَةُ اللهِ", "example_tr": "Selam ve Allah'ın rahmeti üzerinize olsun"},
        {"word_ar": "أَهْلاً وَسَهْلاً",      "word_type": "تحية", "translation_tr": "Hoş geldiniz / Merhaba",       "translation_en": "Welcome",                    "example_ar": "أَهْلاً وَسَهْلاً بِكَ",               "example_tr": "Seni bekliyorduk"},
        {"word_ar": "مَعَ السَّلَامَة",        "word_type": "تحية", "translation_tr": "Güle güle / Allah'a emanet",   "translation_en": "Goodbye",                    "example_ar": "مَعَ السَّلَامَة يَا صَدِيقِي",        "example_tr": "Güle güle arkadaşım"},

        # أسماء الاستفهام
        {"word_ar": "مَا",      "word_type": "اسم_استفهام", "translation_tr": "Ne / Nedir",     "translation_en": "What",  "example_ar": "مَا اسْمُكَ؟",       "example_tr": "Adın ne?"},
        {"word_ar": "مَنْ",     "word_type": "اسم_استفهام", "translation_tr": "Kim",            "translation_en": "Who",   "example_ar": "مَنْ أَنْتَ؟",       "example_tr": "Sen kimsin?"},
        {"word_ar": "مِنْ أَيْنَ", "word_type": "اسم_استفهام", "translation_tr": "Nereden",       "translation_en": "From where", "example_ar": "مِنْ أَيْنَ أَنْتَ؟", "example_tr": "Nerelisin?"},
        {"word_ar": "كَيْفَ",   "word_type": "اسم_استفهام", "translation_tr": "Nasıl",          "translation_en": "How",   "example_ar": "كَيْفَ حَالُكَ؟",    "example_tr": "Nasılsın?"},
        {"word_ar": "هَلْ",     "word_type": "اسم_استفهام", "translation_tr": "Mı / Mi (soru)", "translation_en": "Is/Are", "example_ar": "هَلْ أَنْتَ تُرْكِيٌّ؟", "example_tr": "Türk müsün?"},

        # الضمائر
        {"word_ar": "أَنَا",  "word_type": "ضمير", "translation_tr": "Ben",   "translation_en": "I",     "example_ar": "أَنَا مُحَمَّد",     "example_tr": "Ben Muhammed'im"},
        {"word_ar": "أَنْتَ", "word_type": "ضمير", "translation_tr": "Sen (erkek)", "translation_en": "You (m)", "example_ar": "أَنْتَ طَالِب",     "example_tr": "Sen öğrencisin"},
        {"word_ar": "أَنْتِ", "word_type": "ضمير", "translation_tr": "Sen (kadın)", "translation_en": "You (f)", "example_ar": "أَنْتِ طَالِبَة",  "example_tr": "Sen öğrencisin"},
        {"word_ar": "هُوَ",  "word_type": "ضمير", "translation_tr": "O (erkek)",  "translation_en": "He",    "example_ar": "هُوَ مُدَرِّس",     "example_tr": "O öğretmen"},
        {"word_ar": "هِيَ",  "word_type": "ضمير", "translation_tr": "O (kadın)",  "translation_en": "She",   "example_ar": "هِيَ طَبِيبَة",     "example_tr": "O doktor"},

        # الأسماء والمهن (مذكر / مؤنث)
        {"word_ar": "اسْم",        "word_type": "اسم",  "gender": "مذكر", "translation_tr": "İsim / Ad",    "translation_en": "Name",      "example_ar": "مَا اسْمُكَ؟",          "example_tr": "Adın ne?"},
        {"word_ar": "جِنْسِيَّة",   "word_type": "اسم",  "gender": "مؤنث", "translation_tr": "Milliyet / Uyruk", "translation_en": "Nationality", "example_ar": "مَا جِنْسِيَّتُكَ؟", "example_tr": "Uyruğun ne?"},
        {"word_ar": "بَلَد",        "word_type": "اسم",  "gender": "مذكر", "plural_ar": "بُلْدَان / بِلَاد", "translation_tr": "Ülke / Memleket", "translation_en": "Country",  "example_ar": "مِنْ أَيِّ بَلَد أَنْتَ؟",  "example_tr": "Hangi ülkedensin?"},
        {"word_ar": "مُدَرِّس",     "word_type": "اسم",  "gender": "مذكر", "plural_ar": "مُدَرِّسُون",     "translation_tr": "Öğretmen (erkek)", "translation_en": "Teacher (m)", "example_ar": "هُوَ مُدَرِّس",            "example_tr": "O öğretmen"},
        {"word_ar": "مُدَرِّسَة",   "word_type": "اسم",  "gender": "مؤنث", "translation_tr": "Öğretmen (kadın)", "translation_en": "Teacher (f)", "example_ar": "هِيَ مُدَرِّسَة",          "example_tr": "O öğretmen"},
        {"word_ar": "طَالِب",       "word_type": "اسم",  "gender": "مذكر", "plural_ar": "طُلَّاب",          "translation_tr": "Öğrenci (erkek)", "translation_en": "Student (m)", "example_ar": "أَنَا طَالِب",              "example_tr": "Ben öğrenciyim"},
        {"word_ar": "طَالِبَة",     "word_type": "اسم",  "gender": "مؤنث", "translation_tr": "Öğrenci (kadın)", "translation_en": "Student (f)", "example_ar": "أَنَا طَالِبَة",            "example_tr": "Ben öğrenciyim"},
        {"word_ar": "طَبِيب",       "word_type": "اسم",  "gender": "مذكر", "plural_ar": "أَطِبَّاء",        "translation_tr": "Doktor (erkek)", "translation_en": "Doctor (m)", "example_ar": "أَخِي طَبِيب",              "example_tr": "Ağabeyim doktor"},
        {"word_ar": "طَبِيبَة",     "word_type": "اسم",  "gender": "مؤنث", "translation_tr": "Doktor (kadın)", "translation_en": "Doctor (f)", "example_ar": "أُخْتِي طَبِيبَة",          "example_tr": "Kız kardeşim doktor"},
        {"word_ar": "مُهَنْدِس",    "word_type": "اسم",  "gender": "مذكر", "plural_ar": "مُهَنْدِسُون",    "translation_tr": "Mühendis (erkek)", "translation_en": "Engineer (m)", "example_ar": "أَبِي مُهَنْدِس",         "example_tr": "Babam mühendis"},
        {"word_ar": "مُهَنْدِسَة",  "word_type": "اسم",  "gender": "مؤنث", "translation_tr": "Mühendis (kadın)", "translation_en": "Engineer (f)", "example_ar": "هِيَ مُهَنْدِسَة",        "example_tr": "O mühendis"},
        {"word_ar": "أَخ",          "word_type": "اسم",  "gender": "مذكر", "plural_ar": "إِخْوَة",          "translation_tr": "Erkek kardeş / ağabey", "translation_en": "Brother", "example_ar": "هَذَا أَخِي",           "example_tr": "Bu ağabeyim"},
        {"word_ar": "أُخْت",        "word_type": "اسم",  "gender": "مؤنث", "plural_ar": "أَخَوَات",         "translation_tr": "Kız kardeş",    "translation_en": "Sister",    "example_ar": "هَذِهِ أُخْتِي",            "example_tr": "Bu kız kardeşim"},
        {"word_ar": "صَدِيق",       "word_type": "اسم",  "gender": "مذكر", "plural_ar": "أَصْدِقَاء",       "translation_tr": "Arkadaş (erkek)", "translation_en": "Friend (m)", "example_ar": "هَذَا صَدِيقِي",           "example_tr": "Bu arkadaşım"},
        {"word_ar": "صَدِيقَة",     "word_type": "اسم",  "gender": "مؤنث", "translation_tr": "Arkadaş (kadın)", "translation_en": "Friend (f)", "example_ar": "هَذِهِ صَدِيقَتِي",        "example_tr": "Bu arkadaşım"},

        # الجنسيات والبلدان
        {"word_ar": "تُرْكِيَا",     "word_type": "اسم",  "translation_tr": "Türkiye",  "translation_en": "Turkey",   "example_ar": "أَنَا مِنْ تُرْكِيَا",     "example_tr": "Türkiye'denim"},
        {"word_ar": "تُرْكِيّ",      "word_type": "صفة",  "gender": "مذكر", "translation_tr": "Türk (erkek)", "translation_en": "Turkish (m)", "example_ar": "أَنَا تُرْكِيٌّ",          "example_tr": "Ben Türküm"},
        {"word_ar": "تُرْكِيَّة",    "word_type": "صفة",  "gender": "مؤنث", "translation_tr": "Türk (kadın)", "translation_en": "Turkish (f)", "example_ar": "أَنَا تُرْكِيَّة",         "example_tr": "Ben Türküm"},
        {"word_ar": "مِصْر",         "word_type": "اسم",  "translation_tr": "Mısır",    "translation_en": "Egypt",    "example_ar": "هِيَ مِنْ مِصْر",          "example_tr": "O Mısır'dan"},
        {"word_ar": "مِصْرِيّ",      "word_type": "صفة",  "gender": "مذكر", "translation_tr": "Mısırlı (erkek)", "translation_en": "Egyptian (m)"},
        {"word_ar": "مِصْرِيَّة",    "word_type": "صفة",  "gender": "مؤنث", "translation_tr": "Mısırlı (kadın)", "translation_en": "Egyptian (f)"},
        {"word_ar": "بَاكِسْتَان",   "word_type": "اسم",  "translation_tr": "Pakistan", "translation_en": "Pakistan", "example_ar": "هُوَ مِنْ بَاكِسْتَان",     "example_tr": "O Pakistan'dan"},
        {"word_ar": "بَاكِسْتَانِيّ","word_type": "صفة",  "gender": "مذكر", "translation_tr": "Pakistanlı (erkek)", "translation_en": "Pakistani (m)"},
        {"word_ar": "سُورِيَا",      "word_type": "اسم",  "translation_tr": "Suriye",   "translation_en": "Syria",    "example_ar": "هُوَ مِنْ سُورِيَا",        "example_tr": "O Suriye'den"},
        {"word_ar": "سُورِيّ",       "word_type": "صفة",  "gender": "مذكر", "translation_tr": "Suriyeli (erkek)", "translation_en": "Syrian (m)"},

        # كلمات الحال
        {"word_ar": "بِخَيْر",   "word_type": "ظرف", "translation_tr": "İyiyim",       "translation_en": "Fine / Good", "example_ar": "أَنَا بِخَيْر وَالْحَمْدُ لِله", "example_tr": "İyiyim, Allah'a şükür"},
        {"word_ar": "نَعَمْ",    "word_type": "حرف", "translation_tr": "Evet",          "translation_en": "Yes",         "example_ar": "نَعَمْ، أَنَا تُرْكِيّ",         "example_tr": "Evet, Türküm"},
        {"word_ar": "لَا",       "word_type": "حرف", "translation_tr": "Hayır",         "translation_en": "No",          "example_ar": "لَا، أَنَا لَسْتُ مِصْرِيًّا", "example_tr": "Hayır, Mısırlı değilim"},
        {"word_ar": "وَالْحَمْدُ لِله", "word_type": "تحية", "translation_tr": "Elhamdülillah / Allah'a şükür", "translation_en": "Praise be to Allah"},

        # أسماء إشارة
        {"word_ar": "هَذَا",  "word_type": "ضمير", "gender": "مذكر", "translation_tr": "Bu (erkek için)", "translation_en": "This (m)", "example_ar": "هَذَا أَخِي خَالِد",  "example_tr": "Bu erkek kardeşim Halid"},
        {"word_ar": "هَذِهِ", "word_type": "ضمير", "gender": "مؤنث", "translation_tr": "Bu (kadın için)", "translation_en": "This (f)", "example_ar": "هَذِهِ أُخْتِي فَاطِمَة", "example_tr": "Bu kız kardeşim Fatima"},
    ],

    # ================================================================
    # الحوارات (Dialogues)
    # ================================================================
    "dialogues": [
        {
            "lesson_number": 1,
            "dialogue_number": 1,
            "title_ar": "الحِوَارُ الأَوَّل (أ)",
            "situation_tr": "İki erkek birbirini selamlıyor ve tanışıyor",
            "lines": [
                {"speaker": "خَالِد", "text_ar": "السَّلَامُ عَلَيْكُم",              "translation_tr": "Selam olsun üzerinize",          "is_key": True},
                {"speaker": "خَلِيل", "text_ar": "وَعَلَيْكُمُ السَّلَام",            "translation_tr": "Selam üzerinize de olsun",       "is_key": True},
                {"speaker": "خَالِد", "text_ar": "اسْمِي خَالِد، مَا اسْمُكَ؟",     "translation_tr": "Adım Halid, adın ne?",           "is_key": True},
                {"speaker": "خَلِيل", "text_ar": "اسْمِي خَلِيل",                    "translation_tr": "Adım Halil",                     "is_key": False},
                {"speaker": "خَالِد", "text_ar": "كَيْفَ حَالُكَ؟",                   "translation_tr": "Nasılsın?",                      "is_key": True},
                {"speaker": "خَلِيل", "text_ar": "بِخَيْر، وَالْحَمْدُ لِله",        "translation_tr": "İyiyim, elhamdülillah",          "is_key": True},
                {"speaker": "خَلِيل", "text_ar": "وَكَيْفَ حَالُكَ أَنْتَ؟",         "translation_tr": "Ya sen nasılsın?",               "is_key": False},
                {"speaker": "خَالِد", "text_ar": "بِخَيْر، وَالْحَمْدُ لِله",        "translation_tr": "İyiyim, elhamdülillah",          "is_key": False},
            ]
        },
        {
            "lesson_number": 2,
            "dialogue_number": 2,
            "title_ar": "الحِوَارُ الثَّانِي (أ)",
            "situation_tr": "Nereden olduğunu sorma ve cevaplama",
            "lines": [
                {"speaker": "مُحَمَّد", "text_ar": "السَّلَامُ عَلَيْكُم",                  "translation_tr": "Selam",                      "is_key": False},
                {"speaker": "شَرِيف",  "text_ar": "وَعَلَيْكُمُ السَّلَام",                "translation_tr": "Ve selam",                   "is_key": False},
                {"speaker": "مُحَمَّد", "text_ar": "مِنْ أَيْنَ أَنْتَ؟",                   "translation_tr": "Nerelisin?",                 "is_key": True},
                {"speaker": "شَرِيف",  "text_ar": "أَنَا مِنْ بَاكِسْتَان",                "translation_tr": "Pakistan'danım",             "is_key": True},
                {"speaker": "مُحَمَّد", "text_ar": "هَلْ أَنْتَ بَاكِسْتَانِيٌّ؟",         "translation_tr": "Pakistanlı mısın?",          "is_key": True},
                {"speaker": "شَرِيف",  "text_ar": "نَعَمْ، أَنَا بَاكِسْتَانِيٌّ، وَمَا جِنْسِيَّتُكَ أَنْتَ؟", "translation_tr": "Evet, Pakistanlıyım. Ya senin uyruğun ne?", "is_key": True},
                {"speaker": "مُحَمَّد", "text_ar": "أَنَا تُرْكِيٌّ، أَنَا مِنْ تُرْكِيَا", "translation_tr": "Ben Türküm, Türkiye'denim", "is_key": True},
                {"speaker": "شَرِيف",  "text_ar": "أَهْلاً وَسَهْلاً",                     "translation_tr": "Hoş geldin",                 "is_key": True},
            ]
        },
    ],

    # ================================================================
    # التمارين (Exercises) — وحدة 1
    # ================================================================
    "exercises": [

        # --- اختيار من متعدد ---
        {
            "type": "multiple_choice",
            "question_ar": "مَا مَعْنَى «السَّلَامُ عَلَيْكُم» بِالتُّرْكِيَّة؟",
            "question_tr": "«السلام عليكم» kelimesinin Türkçe anlamı nedir?",
            "correct_answer": "Selam olsun üzerinize",
            "options": ["Günaydın", "Selam olsun üzerinize", "Hoş geldiniz", "Nasılsın"],
            "explanation_ar": "السَّلَامُ عَلَيْكُم هي تحية إسلامية تعني الاطمئنان والسلام على المخاطَب",
            "difficulty": 1, "points": 10
        },
        {
            "type": "multiple_choice",
            "question_ar": "مَا الرَّدُّ الصَّحِيحُ عَلَى «السَّلَامُ عَلَيْكُم»؟",
            "question_tr": "«السلام عليكم» selamına doğru cevap nedir?",
            "correct_answer": "وَعَلَيْكُمُ السَّلَام",
            "options": ["أَهْلاً وَسَهْلاً", "بِخَيْر", "وَعَلَيْكُمُ السَّلَام", "نَعَمْ"],
            "explanation_ar": "الرد الصحيح هو وعليكم السلام أو وعليكم السلام ورحمة الله وبركاته",
            "difficulty": 1, "points": 10
        },
        {
            "type": "multiple_choice",
            "question_ar": "أَيُّ سُؤَالٍ نَسْأَلُ لِمَعْرِفَةِ اسْمِ شَخْص؟",
            "question_tr": "Bir kişinin adını öğrenmek için hangi soruyu sorarız?",
            "correct_answer": "مَا اسْمُكَ؟",
            "options": ["كَيْفَ حَالُكَ؟", "مَا اسْمُكَ؟", "مِنْ أَيْنَ أَنْتَ؟", "هَلْ أَنْتَ تُرْكِيٌّ؟"],
            "difficulty": 1, "points": 10
        },
        {
            "type": "multiple_choice",
            "question_ar": "أَيُّ سُؤَالٍ يَسْأَلُ عَنِ الصِّحَّةِ وَالْحَال؟",
            "question_tr": "Sağlık durumu hakkında hangi soru sorulur?",
            "correct_answer": "كَيْفَ حَالُكَ؟",
            "options": ["مَا اسْمُكَ؟", "مِنْ أَيْنَ أَنْتَ؟", "كَيْفَ حَالُكَ؟", "مَا جِنْسِيَّتُكَ؟"],
            "difficulty": 1, "points": 10
        },
        {
            "type": "multiple_choice",
            "question_ar": "الصِّيغَةُ الصَّحِيحَةُ لِلطَّالِبَةِ: أَنَا ...",
            "question_tr": "Kadın öğrenci için doğru form nedir?",
            "correct_answer": "طَالِبَة",
            "options": ["طَالِب", "طَالِبَة", "مُدَرِّس", "مُدَرِّسَة"],
            "hint_tr": "Arapçada kadın için -ة eki kullanılır",
            "explanation_ar": "المؤنث يأتي بتاء التأنيث في نهاية الكلمة: طَالِب (مذكر) ← طَالِبَة (مؤنث)",
            "difficulty": 2, "points": 15
        },

        # --- إكمال الفراغ ---
        {
            "type": "fill_blank",
            "question_ar": "اسْمِي مُحَمَّد. ___ مِنْ تُرْكِيَا.",
            "question_tr": "Cümleyi tamamla: İsmim Muhammed. ___ Türkiye'denim.",
            "correct_answer": "أَنَا",
            "hint_ar": "الضمير المنفصل للمتكلم",
            "hint_tr": "Birinci tekil şahıs zamiri",
            "difficulty": 1, "points": 10
        },
        {
            "type": "fill_blank",
            "question_ar": "مِنْ أَيْنَ ___ يَا خَالِد؟",
            "question_tr": "Cümleyi tamamla: Nerelisin ya Halid?",
            "correct_answer": "أَنْتَ",
            "hint_ar": "ضمير المخاطب المذكر",
            "hint_tr": "Erkek muhatap zamiri",
            "difficulty": 1, "points": 10
        },
        {
            "type": "fill_blank",
            "question_ar": "السَّلَامُ عَلَيْكُم. — ___ السَّلَام.",
            "question_tr": "Selamı tamamla",
            "correct_answer": "وَعَلَيْكُمُ",
            "explanation_ar": "الرد الكامل: وَعَلَيْكُمُ السَّلَام",
            "difficulty": 1, "points": 10
        },
        {
            "type": "fill_blank",
            "question_ar": "هِيَ لَيْسَتْ مُدَرِّسًا، هِيَ ___.",
            "question_tr": "O öğretmen değil, o ___.",
            "correct_answer": "مُدَرِّسَة",
            "hint_tr": "Kadın için öğretmen kelimesini yaz",
            "difficulty": 2, "points": 15
        },

        # --- ترجمة عربي - تركي ---
        {
            "type": "translate_ar_tr",
            "question_ar": "تَرْجِمْ إِلَى اللُّغَةِ التُّرْكِيَّة: كَيْفَ حَالُكَ؟",
            "correct_answer": "Nasılsın?",
            "hint_tr": "Hal sorusunu çevir",
            "difficulty": 1, "points": 10
        },
        {
            "type": "translate_ar_tr",
            "question_ar": "تَرْجِمْ إِلَى التُّرْكِيَّة: أَنَا طَالِب فِي كُلِّيَّةِ الإِلَهِيَّات",
            "correct_answer": "Ben İlahiyat Fakültesi'nde öğrenciyim",
            "difficulty": 2, "points": 15
        },

        # --- ترجمة تركي - عربي ---
        {
            "type": "translate_tr_ar",
            "question_tr": "Türkçeden Arapçaya çevir: Adım Ahmed, Türkiye'denim.",
            "question_ar": "تَرْجِمْ مِنَ التُّرْكِيَّةِ إِلَى الْعَرَبِيَّة: Adım Ahmed, Türkiye'denim.",
            "correct_answer": "اسْمِي أَحْمَد، أَنَا مِنْ تُرْكِيَا",
            "difficulty": 2, "points": 20
        },
        {
            "type": "translate_tr_ar",
            "question_tr": "Arapçaya çevir: O Mısır'dan, Mısırlı.",
            "question_ar": "تَرْجِمْ إِلَى الْعَرَبِيَّة: O Mısır'dan, Mısırlı.",
            "correct_answer": "هُوَ مِنْ مِصْر، هُوَ مِصْرِيّ",
            "difficulty": 2, "points": 20
        },

        # --- صح وخطأ ---
        {
            "type": "true_false",
            "question_ar": "الرَّدُّ الصَّحِيحُ عَلَى «كَيْفَ حَالُكَ؟» هُوَ «أَهْلاً وَسَهْلاً»",
            "question_tr": "«كيف حالك؟» sorusunun doğru cevabı «أهلاً وسهلاً» mıdır?",
            "correct_answer": "خَطَأ",
            "explanation_ar": "الرد الصحيح هو «بِخَيْر وَالْحَمْدُ لِله»، أما «أَهْلاً وَسَهْلاً» فهي تحية الترحيب",
            "difficulty": 1, "points": 10
        },
        {
            "type": "true_false",
            "question_ar": "«مُدَرِّسَة» هي صيغة المؤنث من «مُدَرِّس»",
            "question_tr": "«مدرسة» kelimesi «مدرس» kelimesinin dişil hali midir?",
            "correct_answer": "صَحِيح",
            "explanation_ar": "نعم، تاء التأنيث تُحوِّل المذكر إلى مؤنث: مُدَرِّس ← مُدَرِّسَة",
            "difficulty": 1, "points": 10
        },

        # --- وصل ---
        {
            "type": "match",
            "question_ar": "صِلْ كُلَّ سُؤَالٍ بِالإِجَابَةِ الْمُنَاسِبَة",
            "question_tr": "Her soruyu uygun cevabıyla eşleştir",
            "correct_answer": "1-c,2-a,3-d,4-b",
            "options": {
                "questions": [
                    "1. مَا اسْمُكَ؟",
                    "2. كَيْفَ حَالُكَ؟",
                    "3. مِنْ أَيْنَ أَنْتَ؟",
                    "4. مَا جِنْسِيَّتُكَ؟"
                ],
                "answers": [
                    "a. بِخَيْر وَالْحَمْدُ لِله",
                    "b. أَنَا تُرْكِيّ",
                    "c. اسْمِي أَحْمَد",
                    "d. أَنَا مِنْ تُرْكِيَا"
                ]
            },
            "difficulty": 2, "points": 20
        },

        # --- كوّن جملة ---
        {
            "type": "form_sentence",
            "question_ar": "رَتِّبِ الْكَلِمَاتِ لِتَكْوِينِ جُمْلَةٍ صَحِيحَة: [تُرْكِيَا / أَنَا / مِنْ]",
            "question_tr": "Kelimeleri doğru cümle oluşturacak şekilde sırala: [تُرْكِيَا / أَنَا / مِنْ]",
            "correct_answer": "أَنَا مِنْ تُرْكِيَا",
            "hint_ar": "ابدأ بالضمير",
            "difficulty": 1, "points": 15
        },
        {
            "type": "form_sentence",
            "question_ar": "كَوِّنْ جُمْلَةً بِاسْتِخْدَامِ: [هِيَ / مُدَرِّسَة / مِصْر / مِنْ]",
            "question_tr": "Şu kelimeleri kullanarak cümle kur: [هِيَ / مُدَرِّسَة / مِصْر / مِنْ]",
            "correct_answer": "هِيَ مُدَرِّسَة مِنْ مِصْر",
            "difficulty": 2, "points": 20
        },

        # --- أجب عن الأسئلة ---
        {
            "type": "respond",
            "question_ar": "أَجِبْ بِاسْمِكَ الْحَقِيقِيّ: مَا اسْمُكَ؟",
            "question_tr": "Kendi gerçek adınla cevapla: Adın ne?",
            "correct_answer": "اسْمِي [اسمك]",
            "hint_ar": "ابدأ بـ «اسْمِي»",
            "hint_tr": "«اسمي» ile başla",
            "difficulty": 1, "points": 10
        },
        {
            "type": "respond",
            "question_ar": "أَجِبْ بِالْعَرَبِيَّة: هَلْ أَنْتَ تُرْكِيٌّ / تُرْكِيَّة؟",
            "question_tr": "Arapça olarak cevapla: Türk müsün?",
            "correct_answer": "نَعَمْ، أَنَا تُرْكِيٌّ / نَعَمْ، أَنَا تُرْكِيَّة",
            "hint_ar": "استخدم «نَعَمْ» أو «لَا» ثم أكمل",
            "difficulty": 1, "points": 10
        },
    ],

    # ================================================================
    # قواعد النحو في هذه الوحدة
    # ================================================================
    "grammar_points": [
        {
            "title_ar": "أسماء الاستفهام الأساسية",
            "title_tr": "Temel soru kelimeleri",
            "explanation_ar": "تُستخدم أسماء الاستفهام للسؤال: مَا (ما هو؟) / مِنْ أَيْنَ (من أين؟) / كَيْفَ (كيف؟) / هَلْ (هل؟) / مَنْ (من؟)",
            "explanation_tr": "Soru kelimeleri: ما = ne, من أين = nereden, كيف = nasıl, هل = mı/mi, من = kim",
            "examples": [
                {"ar": "مَا اسْمُكَ؟", "tr": "Adın ne?"},
                {"ar": "مِنْ أَيْنَ أَنْتَ؟", "tr": "Nerelisin?"},
                {"ar": "كَيْفَ حَالُكَ؟", "tr": "Nasılsın?"},
                {"ar": "هَلْ أَنْتَ تُرْكِيٌّ؟", "tr": "Türk müsün?"},
            ]
        },
        {
            "title_ar": "المذكر والمؤنث في الأسماء",
            "title_tr": "İsimde eril ve dişil",
            "explanation_ar": "يتميز المؤنث بزيادة تاء التأنيث (ة) في الآخر: طَالِب ← طَالِبَة / مُدَرِّس ← مُدَرِّسَة / طَبِيب ← طَبِيبَة",
            "explanation_tr": "Dişil için kelimenin sonuna (ة) eki getirilir",
            "examples": [
                {"ar": "طَالِب / طَالِبَة", "tr": "Öğrenci (erkek) / Öğrenci (kadın)"},
                {"ar": "مُدَرِّس / مُدَرِّسَة", "tr": "Öğretmen (erkek) / Öğretmen (kadın)"},
                {"ar": "مُهَنْدِس / مُهَنْدِسَة", "tr": "Mühendis (erkek) / Mühendis (kadın)"},
            ]
        },
        {
            "title_ar": "الجملة الاسمية البسيطة",
            "title_tr": "Basit isim cümlesi",
            "explanation_ar": "الجملة الاسمية = مبتدأ + خبر، بدون فعل «يكون» في المضارع: أَنَا طَالِب / هُوَ مُدَرِّس / هِيَ مِنْ مِصْر",
            "explanation_tr": "Arapçada şimdiki zaman için 'olmak' fiili kullanılmaz: أنا طالب = Ben öğrenciyim",
            "examples": [
                {"ar": "أَنَا طَالِب", "tr": "Ben öğrenciyim"},
                {"ar": "هُوَ مُدَرِّس", "tr": "O öğretmen(dir)"},
                {"ar": "هِيَ مِنْ مِصْر", "tr": "O Mısır'dan(dır)"},
            ]
        },
    ]
}

if __name__ == "__main__":
    import json
    print(f"الوحدة: {UNIT_1['title_ar']}")
    print(f"عدد المفردات: {len(UNIT_1['vocabulary'])}")
    print(f"عدد الحوارات: {len(UNIT_1['dialogues'])}")
    print(f"عدد التمارين: {len(UNIT_1['exercises'])}")
    print(f"عدد نقاط النحو: {len(UNIT_1['grammar_points'])}")
    print("\nأنواع التمارين:")
    from collections import Counter
    types = Counter(ex['type'] for ex in UNIT_1['exercises'])
    for t, count in types.items():
        print(f"  {t}: {count}")
