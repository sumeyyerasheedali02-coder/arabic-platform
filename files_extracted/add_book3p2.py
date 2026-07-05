content = open('seed_database.py', 'r', encoding='utf-8').read()

if 'BOOK_3_PART_2' in content:
    print('⚠️  BOOK_3_PART_2 موجود مسبقاً')
else:
    content = content.replace(
        'from book3_part1_data import BOOK_3_PART_1',
        'from book3_part1_data import BOOK_3_PART_1\nfrom book3_part2_data import BOOK_3_PART_2'
    )
    content = content.replace(
        'b3p1 = BOOK_3_PART_1["units"]\n        all_units = b1p1 + b1p2 + b2p1 + b2p2 + b3p1',
        'b3p1 = BOOK_3_PART_1["units"]\n        b3p2 = BOOK_3_PART_2["units"]\n        all_units = b1p1 + b1p2 + b2p1 + b2p2 + b3p1 + b3p2'
    )
    if 'BOOK_3_PART_2' in content and 'b3p2' in content:
        open('seed_database.py', 'w', encoding='utf-8').write(content)
        print('✅ نجح التعديل! BOOK_3_PART_2 أُضيف')
        print('   الآن شغّلي: python seed_database.py')
    else:
        print('❌ فشل التعديل')
