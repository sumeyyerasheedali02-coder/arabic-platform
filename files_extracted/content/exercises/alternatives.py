"""Extra accepted answers for bank exercises, found from what students actually typed.

Students repeatedly gave an answer that is right but was not listed (a synonym, a
second translation, another word that fits the blank). Each was reviewed one by one
and is added here, never to the vocabulary or the dialogues.

    (unit, exercise number): (a piece of the question, "alternative / alternative")

The piece of the question is a guard: if the bank changes and the number points to
another exercise, building the bank fails instead of accepting a wrong answer.
Alternatives are separated by « / » like in the bank, and are added to the answer
already there (see content/exercises/bank.py).
"""

ALTERNATIVES = {
    # ── Book 1 ──────────────────────────────────────────────────────────────
    (1, 1107): ("سَعِيد", "فَرِح"),
    (1, 1109): ("طَبِيب", "حَكِيم"),
    (1, 1703): ("اسْمِي", "Adım / İsmim / Benim ismim"),
    (1, 1706): ("iyiyim", "أَنَا بِخَيْر"),
    (1, 1707): ("وَالحَمْدُ لله", "Elhamdülillah"),
    (2, 1110): ("رَأَى", "نَظَرَ"),
    (2, 1501): ("هذا أبي", "هِيَ"),
    (2, 1503): ("أخو أمّي", "خَالٌ"),
    (2, 1504): ("أخو أبي", "عَمٌّ"),
    (4, 1701): ("يَسْتَيْقِظُ", "Uyanıyor / Uyanmak"),
    (5, 1107): ("كَثِير", "عَدِيد"),
    (5, 1307): ("سَمَكَة", "سَمَكَات"),
    (6, 1105): ("يُسَافِرُ", "يَرْتَحِلُ"),
    (6, 1605): ("أفضل / المسجد", "أفضل الصلاة في المسجد"),
    (7, 1207): ("مُبَكِّر", "مُتَأَخِّرًا"),
    (7, 1503): ("غدًا", "اخْتِبَارُ"),
    (7, 1704): ("sınıf", "الصَّفّ / صَفّ"),
    (8, 1102): ("المِهْنَة", "العَمَل"),
    (8, 1105): ("يُحِبُّ", "يَعْشَقُ"),
    (8, 1304): ("صَيْدَلِيّ", "صَيْدَلِيُّون"),
    (8, 1507): ("أذهبُ إلى العمل", "كُلَّ يَوْمٍ"),
    (8, 1702): ("hemşire", "مُمَرِّض"),
    (8, 1704): ("eczacı", "صَيْدَلِيّ"),
    (9, 1109): ("قَلِيل", "يَسِير"),
    (9, 1710): ("Yumurta tabağı", "طَبَقُ البَيْضِ"),
    # ── Book 1, part 2 ──────────────────────────────────────────────────────
    (10, 1205): ("الحَرّ", "بَارِد"),
    (10, 1310): ("سَحَابَة", "سَحَابَات"),
    (10, 1501): ("الجوُّ", "حَرٌّ"),
    (10, 1502): ("الجوُّ", "بَرْدٌ"),
    (10, 1708): ("Sıcak", "حَارّ"),
    (11, 1101): ("انْتَقَلَ", "تَحَوَّلَ"),
    (11, 1502): ("المطار", "السَّيَّارَةِ / الحَافِلَةِ / الباصِ / القِطَارِ"),
    (11, 1505): ("تستغرقُ الرحلةُ", "وَاحِدَةً"),
    (11, 1602): ("جميلة / مدينة / جدة", "مدينة جميلة جدة"),
    (11, 1707): ("يَقْضِي الوَقْت", "Vakit geçirmek / Vakit geçiriyor"),
    (11, 1708): ("Yolculuk", "سَفَر"),
    (11, 1709): ("تَسْتَغْرِق", "Sürüyor / Sürmek"),
    (12, 1109): ("جَمِيل", "حَسَن"),
    (12, 1707): ("السَّفَر", "Yolculuk"),
    (14, 1701): ("يَعْتَمِر", "Umre yapıyor / Umre yapmak"),
}
