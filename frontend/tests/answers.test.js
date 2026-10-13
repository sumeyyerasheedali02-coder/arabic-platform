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
