import assert from 'node:assert/strict'
import { test } from 'node:test'
import { isCorrectAnswer, isTypedExercise, normalizeAnswer } from '../src/features/exercises/answers.js'

// The same cases as files_extracted/tests/test_exercises.py: guests are checked
// here, logged-in students on the server, and both must agree.

test('diacritics and tatweel are ignored', () => {
  assert.equal(normalizeAnswer('عَلَيْكُم'), 'عليكم')
  assert.equal(normalizeAnswer('كتـــاب'), 'كتاب')
  assert.ok(isCorrectAnswer('عليكم', 'عَلَيْكُم'))
})

test('outer spaces and letter case are ignored', () => {
  assert.ok(isCorrectAnswer('  KITAP ', 'kitap'))
  assert.ok(isCorrectAnswer('صحيح', 'صَحِيح'))
})

test('different words are different', () => {
  assert.equal(isCorrectAnswer('شكرا', 'عَلَيْكُم'), false)
  assert.equal(isCorrectAnswer('', 'kitap'), false)
  assert.equal(isCorrectAnswer(undefined, 'kitap'), false)
})

test('the order of combining marks does not matter', () => {
  const shaddaFirst = 'رَتِّب'
  const kasraFirst = 'رَتِّب'
  assert.notEqual(shaddaFirst, kasraFirst)
  assert.ok(isCorrectAnswer(shaddaFirst, kasraFirst))
})

test('initial alef variants are accepted in every word, including decomposed Unicode', () => {
  for (const [given, expected] of [
    ['انا', 'أَنَا'], ['الى', 'إِلَى'], ['آنا', 'أَنَا'], ['ٱسم', 'اسم'],
    ['انا اذهب الى احمد', 'أَنَا أَذْهَبُ إِلَى أَحْمَد'],
    ['(الى) احمد', '(إِلَى) أَحْمَد'], ['ا\u0655لى', 'إِلَى'],
    ['سا\u0654ل', 'سَأَلَ'], ['هذا', 'هَٰذَا'],
  ]) assert.ok(isCorrectAnswer(given, expected), given)
})

test('different letters and noninitial hamza remain significant', () => {
  for (const [given, expected] of [
    ['سال', 'سَأَلَ'], ['بدا', 'بَدَأَ'], ['على', 'إِلَى'],
  ]) assert.equal(isCorrectAnswer(given, expected), false)
})

test('punctuation and repeated spaces are ignored', () => {
  assert.ok(isCorrectAnswer('من اين انت', 'مِنْ أَيْنَ أَنْتَ؟'))
  assert.ok(isCorrectAnswer('اسمي   خالد.', 'اسمي خالد'))
  assert.ok(isCorrectAnswer('«بيت»', 'بيت'))
})

test('each listed alternative is accepted, and so is the whole answer', () => {
  assert.ok(isCorrectAnswer('Köy', 'Kırsal / Köy'))
  assert.ok(isCorrectAnswer('kırsal', 'Kırsal / Köy'))
  assert.ok(isCorrectAnswer('Kırsal / Köy', 'Kırsal / Köy'))
  assert.equal(isCorrectAnswer('Şehir', 'Kırsal / Köy'), false)
  assert.equal(isCorrectAnswer('/', 'Kırsal / Köy'), false)
})

test('Turkish dotted and dotless i are not told apart', () => {
  assert.ok(isCorrectAnswer('kiz', 'kız'))
  assert.ok(isCorrectAnswer('İYİ', 'iyi'))
  assert.ok(isCorrectAnswer('KITAP', 'kitap'))
  assert.ok(isCorrectAnswer('Selamün aleyküm', 'Selâmün aleyküm'))
})

test('the alef after «ال» and its prefixes counts as a word-initial alef', () => {
  assert.ok(isCorrectAnswer('الاخت', 'الأَخْت'))
  assert.ok(isCorrectAnswer('والافطار', 'وَالإِفْطَارُ'))
  assert.ok(isCorrectAnswer('للام', 'لِلْأُمِّ'))
})

test('a final ة/ه and ى/ي are typed alike, inside a word they differ', () => {
  assert.ok(isCorrectAnswer('غرفه', 'غُرْفَةِ'))
  assert.ok(isCorrectAnswer('مستشفي', 'مُسْتَشْفَى'))
  assert.ok(isCorrectAnswer('هى', 'هِيَ'))
  assert.ok(isCorrectAnswer('الساعه الان', 'السَّاعَةَ الآنَ'))
  assert.equal(isCorrectAnswer('سال', 'سَأَلَ'), false)
  assert.equal(isCorrectAnswer('بدا', 'بَدَأَ'), false)
  assert.equal(isCorrectAnswer('مكتبه', 'مَكْتَبٌ'), false)
})

test('typed answers ignore the article of a single word, picking an option does not', () => {
  assert.ok(isCorrectAnswer('قلم', 'القَلَمِ', true))
  assert.ok(isCorrectAnswer('القلم', 'قَلَم', true))
  assert.ok(isCorrectAnswer('ام', 'الأم', true))
  assert.equal(isCorrectAnswer('قلم', 'القَلَمِ', false), false)
  assert.equal(isCorrectAnswer('كتاب جميل', 'الكتاب الجميل', true), false)
  assert.equal(isCorrectAnswer('الأب', 'الأم', true), false)
})

test('which exercises are typed', () => {
  assert.ok(isTypedExercise('fill_blank', null) && isTypedExercise('synonym', []))
  assert.ok(!isTypedExercise('multiple_choice', ['أ', 'ب']) && !isTypedExercise('true_false', null))
  assert.ok(!isTypedExercise('match', ['a']) && !isTypedExercise('fill_blank', ['أ', 'ب']))
})

test('ى for ي and a missing madda are not errors anywhere in a word', () => {
  assert.ok(isCorrectAnswer('علىكم', 'عَلَيْكُم'))
  assert.ok(isCorrectAnswer('مدىنه', 'مَدِينَةٌ'))
  assert.ok(isCorrectAnswer('مراه', 'مِرْآة'))
})

test('typed answers ignore spaces, apostrophes and the optional tanwin alef', () => {
  assert.ok(isCorrectAnswer('و عليكم السلام', 'وَعَلَيْكُمُ السَّلَام', true))
  assert.ok(isCorrectAnswer('الحمدلله', 'الحَمْدُ لله', true))
  assert.ok(isCorrectAnswer('عبدالمطلب', 'عَبْدُ المُطَّلِب', true))
  assert.ok(isCorrectAnswer('selamünaleyküm', 'Selâmün aleyküm', true))
  assert.ok(isCorrectAnswer('büyük anne', 'büyükanne', true))
  assert.ok(isCorrectAnswer('allah’a şükür', "Allah'a şükür", true))
  assert.ok(isCorrectAnswer('allaha şükür', "Allah'a şükür", true))
  assert.ok(isCorrectAnswer('مهندس', 'مُهَنْدِسًا', true))
  assert.ok(isCorrectAnswer('مهندسا', 'مُهَنْدِسًا', true))
  assert.ok(isCorrectAnswer('عصا', 'عَصَا', true))
  assert.equal(isCorrectAnswer('مهندس', 'مُهَنْدِسًا'), false)
  assert.equal(isCorrectAnswer('و عليكم السلام', 'وَعَلَيْكُمُ السَّلَام'), false)
  assert.equal(isCorrectAnswer('عليكم السلام', 'وَعَلَيْكُمُ السَّلَام', true), false)
  assert.equal(isCorrectAnswer('السلام عليكم', 'عليكم السلام', true), false)
  assert.equal(isCorrectAnswer('عص', 'عَصَا', true), false)
})
