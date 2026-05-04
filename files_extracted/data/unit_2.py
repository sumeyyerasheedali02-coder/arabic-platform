"""
بيانات الوحدة الثانية: الأسرة والعائلة
مستوحاة من كتاب العربية بين يديك - الجزء الأول
"""

UNIT_2 = {
    "unit_number": 2,
    "title_ar": "الأُسْرَةُ وَالْعَائِلَة",
    "title_tr": "Aile ve Akrabalar",
    "description_ar": "تعلم كيفية التحدث عن أفراد الأسرة والعلاقات العائلية",
    "description_tr": "Aile üyeleri ve akrabalık ilişkileri hakkında konuşmayı öğren",

    # ================================================================
    # المفردات الأساسية للوحدة الثانية
    # ================================================================
    "vocabulary": [

        # ── أفراد الأسرة المباشرة ──
        {"word_ar": "أَب",        "word_type": "اسم", "gender": "مذكر", "plural_ar": "آبَاء",
         "translation_tr": "Baba",        "translation_en": "Father",
         "example_ar": "أَبِي مُدَرِّس",           "example_tr": "Babam öğretmen"},
        {"word_ar": "أُم",        "word_type": "اسم", "gender": "مؤنث", "plural_ar": "أُمَّهَات",
         "translation_tr": "Anne",         "translation_en": "Mother",
         "example_ar": "أُمِّي طَبِيبَة",           "example_tr": "Annem doktor"},
        {"word_ar": "اِبْن",      "word_type": "اسم", "gender": "مذكر", "plural_ar": "أَبْنَاء",
         "translation_tr": "Oğul",         "translation_en": "Son",
         "example_ar": "هَذَا اِبْنُهُ الْكَبِير",  "example_tr": "Bu onun büyük oğlu"},
        {"word_ar": "اِبْنَة",    "word_type": "اسم", "gender": "مؤنث", "plural_ar": "بَنَات",
         "translation_tr": "Kız evlat",    "translation_en": "Daughter",
         "example_ar": "لَهُ اِبْنَة وَاحِدَة",     "example_tr": "Onun bir kızı var"},
        {"word_ar": "زَوْج",      "word_type": "اسم", "gender": "مذكر",
         "translation_tr": "Koca / Eş (erkek)", "translation_en": "Husband",
         "example_ar": "زَوْجُهَا مُهَنْدِس",       "example_tr": "Kocası mühendis"},
        {"word_ar": "زَوْجَة",    "word_type": "اسم", "gender": "مؤنث",
         "translation_tr": "Eş (kadın) / Karı", "translation_en": "Wife",
         "example_ar": "زَوْجَتُهُ مُدَرِّسَة",     "example_tr": "Karısı öğretmen"},

        # ── الأجداد ──
        {"word_ar": "جَد",        "word_type": "اسم", "gender": "مذكر", "plural_ar": "أَجْدَاد",
         "translation_tr": "Büyükbaba / Dede", "translation_en": "Grandfather",
         "example_ar": "جَدِّي فِي السَّبْعِينَ",   "example_tr": "Dedem yetmişinde"},
        {"word_ar": "جَدَّة",     "word_type": "اسم", "gender": "مؤنث",
         "translation_tr": "Büyükanne / Nine", "translation_en": "Grandmother",
         "example_ar": "جَدَّتِي طَيِّبَة جِدًّا",  "example_tr": "Ninem çok iyi kalpli"},

        # ── الأعمام والأخوال ──
        {"word_ar": "عَم",        "word_type": "اسم", "gender": "مذكر", "plural_ar": "أَعْمَام",
         "translation_tr": "Amca (babadan)", "translation_en": "Paternal uncle",
         "example_ar": "عَمِّي يَسْكُن فِي إِسْطَنْبُول", "example_tr": "Amcam İstanbul'da oturuyor"},
        {"word_ar": "عَمَّة",     "word_type": "اسم", "gender": "مؤنث", "plural_ar": "عَمَّات",
         "translation_tr": "Hala (babadan)",  "translation_en": "Paternal aunt",
         "example_ar": "عَمَّتِي مُتَزَوِّجَة",      "example_tr": "Halam evli"},
        {"word_ar": "خَال",       "word_type": "اسم", "gender": "مذكر", "plural_ar": "أَخْوَال",
         "translation_tr": "Dayı (anneden)",  "translation_en": "Maternal uncle",
         "example_ar": "خَالِي طَبِيب",              "example_tr": "Dayım doktor"},
        {"word_ar": "خَالَة",     "word_type": "اسم", "gender": "مؤنث", "plural_ar": "خَالَات",
         "translation_tr": "Teyze (anneden)", "translation_en": "Maternal aunt",
         "example_ar": "خَالَتِي مُدَرِّسَة",        "example_tr": "Teyzem öğretmen"},

        # ── أبناء العم والخال ──
        {"word_ar": "اِبْن عَم",  "word_type": "اسم", "gender": "مذكر",
         "translation_tr": "Erkek kuzen (amca oğlu)", "translation_en": "Male cousin (paternal)",
         "example_ar": "اِبْن عَمِّي فِي الْجَامِعَة", "example_tr": "Amcaoğlum üniversitede"},
        {"word_ar": "اِبْنَة عَم","word_type": "اسم", "gender": "مؤنث",
         "translation_tr": "Kız kuzen (amca kızı)", "translation_en": "Female cousin (paternal)",
         "example_ar": "اِبْنَة عَمِّي طَالِبَة",    "example_tr": "Amcakızım öğrenci"},

        # ── الأرقام ١-١٠ ──
        {"word_ar": "وَاحِد",  "word_type": "عدد", "translation_tr": "Bir",    "translation_en": "One",
         "example_ar": "لِي أَخٌ وَاحِد",            "example_tr": "Bir erkek kardeşim var"},
        {"word_ar": "اِثْنَان","word_type": "عدد", "translation_tr": "İki",    "translation_en": "Two",
         "example_ar": "لِي أُخْتَانِ اِثْنَتَانِ",  "example_tr": "İki kız kardeşim var"},
        {"word_ar": "ثَلَاثَة","word_type": "عدد", "translation_tr": "Üç",    "translation_en": "Three",
         "example_ar": "فِي أُسْرَتِي ثَلَاثَة أَبْنَاء", "example_tr": "Ailede üç çocuk var"},
        {"word_ar": "أَرْبَعَة","word_type": "عدد","translation_tr": "Dört",  "translation_en": "Four",
         "example_ar": "لَهُ أَرْبَعَة إِخْوَة",     "example_tr": "Dört erkek kardeşi var"},
        {"word_ar": "خَمْسَة", "word_type": "عدد", "translation_tr": "Beş",   "translation_en": "Five",
         "example_ar": "الْأُسْرَة مِنْ خَمْسَة أَفْرَاد","example_tr": "Aile beş kişiden oluşuyor"},
        {"word_ar": "سِتَّة",  "word_type": "عدد", "translation_tr": "Altı",  "translation_en": "Six",
         "example_ar": "عِنْدِي سِتَّة أَعْمَام",    "example_tr": "Altı amcam var"},
        {"word_ar": "سَبْعَة", "word_type": "عدد", "translation_tr": "Yedi",  "translation_en": "Seven",
         "example_ar": "فِي الشَّارِع سَبْعَة بُيُوت","example_tr": "Sokakta yedi ev var"},
        {"word_ar": "ثَمَانِيَة","word_type": "عدد","translation_tr": "Sekiz","translation_en": "Eight",
         "example_ar": "عُمُرِي ثَمَانِيَة عَشَر سَنَة","example_tr": "On sekiz yaşındayım"},
        {"word_ar": "تِسْعَة", "word_type": "عدد", "translation_tr": "Dokuz","translation_en": "Nine",
         "example_ar": "السَّاعَة تِسْعَة",          "example_tr": "Saat dokuz"},
        {"word_ar": "عَشَرَة", "word_type": "عدد", "translation_tr": "On",    "translation_en": "Ten",
         "example_ar": "فِي الْفَصْل عَشَرَة طُلَّاب", "example_tr": "Sınıfta on öğrenci var"},

        # ── صفات وصفية ──
        {"word_ar": "كَبِير",     "word_type": "صفة", "gender": "مذكر",
         "translation_tr": "Büyük / Yaşlı", "translation_en": "Big / Old",
         "example_ar": "أَخِي الْأَكْبَر طَبِيب",   "example_tr": "Büyük kardeşim doktor"},
        {"word_ar": "كَبِيرَة",   "word_type": "صفة", "gender": "مؤنث",
         "translation_tr": "Büyük (kadın)", "translation_en": "Big / Old (f)",
         "example_ar": "أُخْتِي الْكَبِيرَة مُتَزَوِّجَة", "example_tr": "Büyük kız kardeşim evli"},
        {"word_ar": "صَغِير",     "word_type": "صفة", "gender": "مذكر",
         "translation_tr": "Küçük / Genç", "translation_en": "Small / Young",
         "example_ar": "أَخِي الصَّغِير فِي الْمَدْرَسَة","example_tr": "Küçük kardeşim okulda"},
        {"word_ar": "صَغِيرَة",   "word_type": "صفة", "gender": "مؤنث",
         "translation_tr": "Küçük (kadın)", "translation_en": "Small / Young (f)",
         "example_ar": "أُخْتِي الصَّغِيرَة جَمِيلَة",  "example_tr": "Küçük kız kardeşim güzel"},
        {"word_ar": "مُتَزَوِّج", "word_type": "صفة", "gender": "مذكر",
         "translation_tr": "Evli (erkek)", "translation_en": "Married (m)",
         "example_ar": "أَخِي مُتَزَوِّج وَلَهُ وَلَدَان","example_tr": "Erkek kardeşim evli ve iki çocuğu var"},
        {"word_ar": "مُتَزَوِّجَة","word_type": "صفة","gender": "مؤنث",
         "translation_tr": "Evli (kadın)", "translation_en": "Married (f)",
         "example_ar": "أُخْتِي مُتَزَوِّجَة",      "example_tr": "Kız kardeşim evli"},
        {"word_ar": "أَعْزَب",    "word_type": "صفة", "gender": "مذكر",
         "translation_tr": "Bekar (erkek)","translation_en": "Single (m)",
         "example_ar": "أَنَا أَعْزَب بَعْد",        "example_tr": "Ben hâlâ bekarım"},
        {"word_ar": "عَزْبَاء",   "word_type": "صفة", "gender": "مؤنث",
         "translation_tr": "Bekar (kadın)","translation_en": "Single (f)",
         "example_ar": "هِيَ عَزْبَاء",              "example_tr": "O bekardır"},

        # ── كلمات مفيدة ──
        {"word_ar": "أُسْرَة",    "word_type": "اسم", "gender": "مؤنث", "plural_ar": "أُسَر",
         "translation_tr": "Aile (çekirdek)", "translation_en": "Family (nuclear)",
         "example_ar": "أُسْرَتِي صَغِيرَة",        "example_tr": "Ailem küçük"},
        {"word_ar": "عَائِلَة",   "word_type": "اسم", "gender": "مؤنث", "plural_ar": "عَائِلَات",
         "translation_tr": "Aile / Soy",     "translation_en": "Family (extended)",
         "example_ar": "عَائِلَتِي كَبِيرَة",       "example_tr": "Ailem büyük"},
        {"word_ar": "كَمْ",       "word_type": "اسم_استفهام",
         "translation_tr": "Kaç (tane)?",    "translation_en": "How many?",
         "example_ar": "كَمْ أَخًا لَكَ؟",         "example_tr": "Kaç erkek kardeşin var?"},
        {"word_ar": "لِي",        "word_type": "حرف_جر",
         "translation_tr": "Benim var",      "translation_en": "I have (lit. for me)",
         "example_ar": "لِي أَخَانِ",               "example_tr": "İki erkek kardeşim var"},
        {"word_ar": "لَهُ",       "word_type": "حرف_جر",
         "translation_tr": "Onun var (erkek)", "translation_en": "He has",
         "example_ar": "لَهُ ثَلَاثَة أَبْنَاء",   "example_tr": "Üç oğlu var"},
        {"word_ar": "لَهَا",      "word_type": "حرف_جر",
         "translation_tr": "Onun var (kadın)", "translation_en": "She has",
         "example_ar": "لَهَا بِنْتَانِ",           "example_tr": "İki kızı var"},
        {"word_ar": "عُمْر",      "word_type": "اسم",  "gender": "مذكر", "plural_ar": "أَعْمَار",
         "translation_tr": "Yaş",             "translation_en": "Age",
         "example_ar": "كَمْ عُمْرُكَ؟",           "example_tr": "Kaç yaşındasın?"},
        {"word_ar": "سَنَة",      "word_type": "اسم",  "gender": "مؤنث", "plural_ar": "سَنَوَات / سِنُون",
         "translation_tr": "Yıl / Sene",      "translation_en": "Year",
         "example_ar": "عُمْرِي عِشْرُون سَنَة",   "example_tr": "Yirmi yaşındayım"},
        {"word_ar": "يَسْكُن",    "word_type": "فعل",
         "translation_tr": "Oturuyor / Yaşıyor", "translation_en": "Lives / Resides",
         "example_ar": "أَبِي يَسْكُن فِي أَنْقَرَة","example_tr": "Babam Ankara'da oturuyor"},
        {"word_ar": "مَعَ",       "word_type": "حرف_جر",
         "translation_tr": "İle / Beraber",   "translation_en": "With",
         "example_ar": "أَنَا أَسْكُن مَعَ أُسْرَتِي","example_tr": "Ailemle birlikte yaşıyorum"},
    ],

    # ================================================================
    # الحوارات (Dialogues)
    # ================================================================
    "dialogues": [
        {
            "lesson_number": 1,
            "dialogue_number": 1,
            "title_ar": "الحِوَارُ الأَوَّل — كَمْ أَخًا لَكَ؟",
            "situation_tr": "İki arkadaş birbirlerinin ailelerini anlatıyor",
            "lines": [
                {"speaker": "أَحْمَد",  "text_ar": "يَا خَالِد، كَمْ أَخًا لَكَ؟",
                 "translation_tr": "Ya Halid, kaç erkek kardeşin var?",       "is_key": True},
                {"speaker": "خَالِد",  "text_ar": "لِي أَخَانِ وَأُخْتٌ وَاحِدَة",
                 "translation_tr": "İki erkek kardeşim ve bir kız kardeşim var", "is_key": True},
                {"speaker": "أَحْمَد",  "text_ar": "هَلْ أَخُوكَ الْكَبِير مُتَزَوِّج؟",
                 "translation_tr": "Büyük erkek kardeşin evli mi?",            "is_key": True},
                {"speaker": "خَالِد",  "text_ar": "نَعَمْ، هُوَ مُتَزَوِّج وَلَهُ وَلَدَان",
                 "translation_tr": "Evet, evli ve iki çocuğu var",            "is_key": True},
                {"speaker": "أَحْمَد",  "text_ar": "وَأُخْتُكَ، هَلْ هِيَ مُتَزَوِّجَة؟",
                 "translation_tr": "Peki kız kardeşin, evli mi?",             "is_key": False},
                {"speaker": "خَالِد",  "text_ar": "لَا، هِيَ عَزْبَاء، هِيَ طَالِبَة فِي الْجَامِعَة",
                 "translation_tr": "Hayır, o bekar, üniversitede öğrenci",   "is_key": True},
                {"speaker": "أَحْمَد",  "text_ar": "وَأَنْتَ، كَمْ عُمْرُكَ؟",
                 "translation_tr": "Peki ya sen, kaç yaşındasın?",           "is_key": True},
                {"speaker": "خَالِد",  "text_ar": "عُمْرِي عِشْرُون سَنَة",
                 "translation_tr": "Yirmi yaşındayım",                       "is_key": True},
            ]
        },
        {
            "lesson_number": 2,
            "dialogue_number": 2,
            "title_ar": "الحِوَارُ الثَّانِي — أَيْنَ يَسْكُن أَبُوكَ؟",
            "situation_tr": "Bir öğrenci ailesini ve nerede oturduklarını anlatıyor",
            "lines": [
                {"speaker": "فَاطِمَة", "text_ar": "يَا مَرْيَم، أَيْنَ تَسْكُنِين؟",
                 "translation_tr": "Ya Meryem, nerede oturuyorsun?",          "is_key": True},
                {"speaker": "مَرْيَم",  "text_ar": "أَنَا أَسْكُن فِي كَارَابُوك مَعَ أُسْرَتِي",
                 "translation_tr": "Karabük'te ailemle birlikte oturuyorum", "is_key": True},
                {"speaker": "فَاطِمَة", "text_ar": "كَمْ فَرْدًا فِي أُسْرَتِكِ؟",
                 "translation_tr": "Ailende kaç kişi var?",                  "is_key": True},
                {"speaker": "مَرْيَم",  "text_ar": "فِي أُسْرَتِي خَمْسَة أَفْرَاد: أَبِي وَأُمِّي وَأَنَا وَأَخِي وَأُخْتِي الصَّغِيرَة",
                 "translation_tr": "Ailemde beş kişi var: babam, annem, ben, kardeşim ve küçük kız kardeşim", "is_key": True},
                {"speaker": "فَاطِمَة", "text_ar": "مَا عَمَل أَبِيكِ؟",
                 "translation_tr": "Babanın mesleği ne?",                    "is_key": True},
                {"speaker": "مَرْيَم",  "text_ar": "أَبِي مُدَرِّس فِي مَدْرَسَة ثَانَوِيَّة",
                 "translation_tr": "Babam lisede öğretmen",                  "is_key": True},
                {"speaker": "فَاطِمَة", "text_ar": "وَأُمُّكِ؟",
                 "translation_tr": "Peki annen?",                            "is_key": False},
                {"speaker": "مَرْيَم",  "text_ar": "أُمِّي رَبَّة بَيْت",
                 "translation_tr": "Annem ev hanımı",                        "is_key": True},
            ]
        },
    ],

    # ================================================================
    # التمارين (Exercises) — وحدة 2
    # ================================================================
    "exercises": [

        # --- اختيار من متعدد ---
        {
            "type": "multiple_choice",
            "question_ar": "مَا مَعْنَى «أَب» بِالتُّرْكِيَّة؟",
            "question_tr": "«أب» kelimesinin Türkçe anlamı nedir?",
            "correct_answer": "Baba",
            "options": ["Anne", "Baba", "Dede", "Amca"],
            "difficulty": 1, "points": 10
        },
        {
            "type": "multiple_choice",
            "question_ar": "مَا مَعْنَى «كَمْ» فِي السُّؤَال؟",
            "question_tr": "Soru cümlesinde «كم» ne anlama gelir?",
            "correct_answer": "Kaç",
            "options": ["Nerede", "Kaç", "Kim", "Ne zaman"],
            "explanation_ar": "كَمْ اسم استفهام للسؤال عن العدد",
            "difficulty": 1, "points": 10
        },
        {
            "type": "multiple_choice",
            "question_ar": "مَا مَعْنَى «عَمَّة»؟",
            "question_tr": "«عمة» ne demektir?",
            "correct_answer": "Hala",
            "options": ["Teyze", "Hala", "Nine", "Abla"],
            "explanation_ar": "العَمَّة هي أُخْت الأَب، أما الخالة فهي أُخْت الأُم",
            "difficulty": 2, "points": 15
        },
        {
            "type": "multiple_choice",
            "question_ar": "أَيُّ جُمْلَة صَحِيحَة لِقَوْل «عِنْدِي ثَلَاثَة أَخَوَات»؟",
            "question_tr": "'Üç kız kardeşim var' cümlesini nasıl söylersiniz?",
            "correct_answer": "لِي ثَلَاث أَخَوَات",
            "options": ["لِي ثَلَاثَة أَخَوَات", "لِي ثَلَاث أَخَوَات", "لِي ثَلَاثَة أُخْوَة", "عِنْدِي ثَلَاث أَخٌ"],
            "explanation_ar": "العدد مع المؤنث يكون بغير تاء التأنيث: ثَلَاث أَخَوَات",
            "difficulty": 3, "points": 15
        },
        {
            "type": "multiple_choice",
            "question_ar": "مَا مَعْنَى «لَهَا أُخْتَانِ»؟",
            "question_tr": "«لها أختان» ne anlama gelir?",
            "correct_answer": "Onun iki kız kardeşi var",
            "options": ["İki kardeşim var", "Onun iki kız kardeşi var", "Onun iki erkek kardeşi var", "İki ablası var"],
            "difficulty": 2, "points": 10
        },

        # --- إكمال الفراغ ---
        {
            "type": "fill_blank",
            "question_ar": "أَبِي مُدَرِّس وَأُمِّي ___.",
            "question_tr": "Babam öğretmen ve annem ___. (doktor)",
            "correct_answer": "طَبِيبَة",
            "hint_ar": "صيغة المؤنث من طبيب",
            "hint_tr": "Doktor kelimesinin dişil hali",
            "difficulty": 1, "points": 10
        },
        {
            "type": "fill_blank",
            "question_ar": "لِي أَخٌ ___ وَأُخْتٌ صَغِيرَة.",
            "question_tr": "Bir ___ erkek kardeşim ve bir küçük kız kardeşim var. (büyük)",
            "correct_answer": "كَبِير",
            "hint_ar": "ضد صغير",
            "difficulty": 1, "points": 10
        },
        {
            "type": "fill_blank",
            "question_ar": "كَمْ ___ لَكَ؟ — لِي ثَلَاثَة إِخْوَة.",
            "question_tr": "Cümleyi tamamla: Kaç ___ var? — Üç erkek kardeşim var.",
            "correct_answer": "أَخًا",
            "hint_ar": "اسم مفرد من إِخْوَة",
            "difficulty": 2, "points": 15
        },
        {
            "type": "fill_blank",
            "question_ar": "أَنَا أَسْكُن ___ أُسْرَتِي فِي كَارَابُوك.",
            "question_tr": "Ben ailem ___ Karabük'te oturuyorum. (ile/beraber)",
            "correct_answer": "مَعَ",
            "hint_tr": "İle / birlikte anlamında bir edat",
            "difficulty": 1, "points": 10
        },

        # --- ترجمة ---
        {
            "type": "translate_ar_tr",
            "question_ar": "تَرْجِمْ: أُسْرَتِي كَبِيرَة، لِي ثَلَاثَة إِخْوَة وَأُخْتَانِ.",
            "correct_answer": "Ailem büyük, üç erkek kardeşim ve iki kız kardeşim var.",
            "hint_tr": "Aile üyesi sayılarına dikkat et",
            "difficulty": 2, "points": 15
        },
        {
            "type": "translate_tr_ar",
            "question_tr": "Arapçaya çevir: Annem ev hanımı, babam öğretmen.",
            "question_ar": "تَرْجِمْ إِلَى الْعَرَبِيَّة: Annem ev hanımı, babam öğretmen.",
            "correct_answer": "أُمِّي رَبَّة بَيْت، أَبِي مُدَرِّس",
            "difficulty": 2, "points": 20
        },

        # --- صح وخطأ ---
        {
            "type": "true_false",
            "question_ar": "«عَمَّة» هِيَ أُخْت الأُم",
            "question_tr": "«عمة» annenin kız kardeşidir",
            "correct_answer": "خَطَأ",
            "explanation_ar": "العَمَّة هي أُخْت الأب، وأُخْت الأُم تُسمَّى خَالَة",
            "difficulty": 2, "points": 10
        },
        {
            "type": "true_false",
            "question_ar": "«لِي» تعني «عندي» أو «بحوزتي»",
            "question_tr": "«لي» kelimesi 'bende var' veya 'benim' anlamına gelir",
            "correct_answer": "صَحِيح",
            "explanation_ar": "لِي = لَدَيَّ = عِنْدِي، تُستخدم للتعبير عن الملكية أو الوجود",
            "difficulty": 1, "points": 10
        },

        # --- كوّن جملة ---
        {
            "type": "form_sentence",
            "question_ar": "رَتِّب: [أُسْرَتِي / خَمْسَة / فِي / أَفْرَاد]",
            "question_tr": "Doğru cümle kur: [أسرتي / خمسة / في / أفراد]",
            "correct_answer": "فِي أُسْرَتِي خَمْسَة أَفْرَاد",
            "hint_ar": "ابدأ بـ «في»",
            "difficulty": 2, "points": 15
        },
        {
            "type": "form_sentence",
            "question_ar": "كَوِّن جُمْلَة: [مُتَزَوِّج / أَخِي / وَلَهُ / وَلَدَان / الْكَبِير]",
            "question_tr": "Cümle kur: [evli / erkek kardeşim / ve onun / iki çocuğu var / büyük]",
            "correct_answer": "أَخِي الْكَبِير مُتَزَوِّج وَلَهُ وَلَدَان",
            "difficulty": 3, "points": 20
        },

        # --- أجب عن السؤال ---
        {
            "type": "respond",
            "question_ar": "أَجِبْ: كَمْ فَرْدًا فِي أُسْرَتِكَ / أُسْرَتِكِ؟",
            "question_tr": "Cevapla: Ailende kaç kişi var?",
            "correct_answer": "فِي أُسْرَتِي [عدد] أَفْرَاد",
            "hint_ar": "استخدم: فِي أُسْرَتِي + العدد + أَفْرَاد",
            "hint_tr": "فِي أُسْرَتِي + sayı + أفراد",
            "difficulty": 1, "points": 10
        },
        {
            "type": "respond",
            "question_ar": "أَجِبْ: هَلْ أَنْتَ مُتَزَوِّج / مُتَزَوِّجَة؟",
            "question_tr": "Cevapla: Evli misin?",
            "correct_answer": "نَعَمْ، أَنَا مُتَزَوِّج / لَا، أَنَا أَعْزَب",
            "hint_ar": "استخدم نعم أو لا ثم الصفة المناسبة",
            "difficulty": 1, "points": 10
        },
    ],

    # ================================================================
    # قواعد النحو في هذه الوحدة
    # ================================================================
    "grammar_points": [
        {
            "title_ar": "ضمائر الملكية (المضاف إليه)",
            "title_tr": "İyelik ekleri",
            "explanation_ar": "نُعبِّر عن الملكية بإضافة ضمير متصل آخر الكلمة: أَب + ي = أَبِي / أَب + كَ = أَبُوكَ / أَب + هُ = أَبُوهُ",
            "explanation_tr": "Sahiplik bildirmek için kelimenin sonuna ek getirilir: أبي = babam، أبوك = babanın، أبوه = onun babası",
            "examples": [
                {"ar": "أَبِي / أُمِّي", "tr": "babam / annem"},
                {"ar": "أَبُوكَ / أُمُّكَ", "tr": "babanın / annenin"},
                {"ar": "أَبُوهُ / أُمُّهُ", "tr": "onun babası / annesi"},
                {"ar": "أُسْرَتِي / أُسْرَتُكَ", "tr": "ailem / ailen"},
            ]
        },
        {
            "title_ar": "الأرقام من ١ إلى ١٠",
            "title_tr": "1'den 10'a kadar sayılar",
            "explanation_ar": "الأرقام في العربية تخالف المعدود في التذكير والتأنيث من ٣ إلى ١٠",
            "explanation_tr": "Arapçada 3-10 arası sayılar sayılan isimle cinsiyette ters çalışır",
            "examples": [
                {"ar": "ثَلَاثَة رِجَال (مذكر)", "tr": "üç erkek"},
                {"ar": "ثَلَاث نِسَاء (مؤنث)", "tr": "üç kadın"},
                {"ar": "خَمْسَة أَوْلَاد", "tr": "beş erkek çocuk"},
                {"ar": "خَمْس بَنَات", "tr": "beş kız çocuk"},
            ]
        },
        {
            "title_ar": "المثنى",
            "title_tr": "İkil (çift) yapısı",
            "explanation_ar": "للدلالة على اثنين نضيف «ان» في حالة الرفع و«ين» في غيرها: أَخٌ → أَخَانِ / أُخْتٌ → أُخْتَانِ",
            "explanation_tr": "İkili yapmak için kelimeye -ان eki getirilir: أخان = iki erkek kardeş، أختان = iki kız kardeş",
            "examples": [
                {"ar": "أَخٌ → أَخَانِ", "tr": "erkek kardeş → iki erkek kardeş"},
                {"ar": "أُخْتٌ → أُخْتَانِ", "tr": "kız kardeş → iki kız kardeş"},
                {"ar": "وَلَدٌ → وَلَدَانِ", "tr": "çocuk → iki çocuk"},
            ]
        },
    ]
}
