import assert from 'node:assert/strict'
import { test } from 'node:test'
import { isCorrectAnswer, normalizeAnswer } from '../src/features/exercises/answers.js'

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
