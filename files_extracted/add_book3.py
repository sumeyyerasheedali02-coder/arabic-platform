"""
add_book3.py - يضيف كتاب 3 جزء 1 إلى seed_database.py
"""
content = open('seed_database.py', 'r', encoding='utf-8').read()

# التحقق من أن الكتاب لم يُضَف مسبقاً
if 'BOOK_3_PART_1' in content:
    print('⚠️  BOOK_3_PART_1 موجود مسبقاً في seed_database.py')
else:
    # إضافة الاستيراد
    content = content.replace(
        'from book2_part2_data import BOOK_2_PART_2',
        'from book2_part2_data import BOOK_2_PART_2\nfrom book3_part1_data import BOOK_3_PART_1'
    )
    # إضافة الوحدات
    content = content.replace(
        'b2p2 = BOOK_2_PART_2["units"]\n        all_units = b1p1 + b1p2 + b2p1 + b2p2',
        'b2p2 = BOOK_2_PART_2["units"]\n        b3p1 = BOOK_3_PART_1["units"]\n        all_units = b1p1 + b1p2 + b2p1 + b2p2 + b3p1'
    )
    
    if 'BOOK_3_PART_1' in content and 'b3p1' in content:
        open('seed_database.py', 'w', encoding='utf-8').write(content)
        print('✅ نجح التعديل! BOOK_3_PART_1 أُضيف إلى seed_database.py')
        print('   الآن شغّلي: python seed_database.py')
    else:
        print('❌ فشل التعديل — النص المطلوب غير موجود')
        print('   تحققي من أن seed_database.py يحتوي على BOOK_2_PART_2')
