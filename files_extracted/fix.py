content = open('seed_database.py', 'r', encoding='utf-8').read()

old1 = 'from book1_part2_data import BOOK_1_PART_2\nfrom book2_part1_data import BOOK_2_PART_1'
new1 = 'from book1_part2_data import BOOK_1_PART_2\nfrom book2_part1_data import BOOK_2_PART_1\nfrom book2_part2_data import BOOK_2_PART_2'

old2 = '        b2p1 = [dict(u, number=u["number"]+16) for u in BOOK_2_PART_1["units"]]\n        all_units = b1p1 + b1p2 + b2p1'
new2 = '        b2p1 = [dict(u, number=u["number"]+16) for u in BOOK_2_PART_1["units"]]\n        b2p2 = BOOK_2_PART_2["units"]\n        all_units = b1p1 + b1p2 + b2p1 + b2p2'

result = content.replace(old1, new1).replace(old2, new2)

if 'BOOK_2_PART_2' in result and 'b2p2' in result:
    open('seed_database.py', 'w', encoding='utf-8').write(result)
    print('✅ تم التعديل بنجاح! الآن شغّلي: python seed_database.py')
else:
    print('❌ لم يتم التعديل — النص المطلوب غير موجود في الملف')
