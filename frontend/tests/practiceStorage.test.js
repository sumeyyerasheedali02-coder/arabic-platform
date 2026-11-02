import assert from 'node:assert/strict'
import { test } from 'node:test'
import { contentKey, newGuestSession, readGuestSessions, saveGuestSession } from '../src/features/exercises/practiceStorage.js'

const exercises = [{ id: 1, question_ar: 'سؤال', correct_answer: 'أ' }, { id: 2, question_ar: 'ثانٍ', correct_answer: 'ب' }]
function memory() {
  const data = new Map()
  return { getItem: k => data.get(k) ?? null, setItem: (k, v) => data.set(k, v) }
}
test('guest feedback and next cursor survive storage roundtrip, independently per unit and filter', () => {
  const store = memory()
  const session = { ...newGuestSession('multiple_choice', exercises), current_index: 1,
    results: [{ exercise_id: 1, is_correct: true, points_earned: 0, student_answer: 'أ' }] }
  assert.equal(saveGuestSession(1, session, store), true)
  assert.deepEqual(readGuestSessions(1, store), [session])
  assert.deepEqual(readGuestSessions(2, store), [])
  saveGuestSession(1, newGuestSession('fill_blank', exercises), store)
  assert.equal(readGuestSessions(1, store).length, 2)
})
test('restart resets only one practice slot; mistakes review excludes correct exercises', () => {
  const store = memory()
  const previous = { ...newGuestSession('multiple_choice', exercises), current_index: 2, completed: true,
    results: [{ exercise_id: 1, is_correct: true }, { exercise_id: 2, is_correct: false }] }
  saveGuestSession(1, previous, store)
  const review = newGuestSession('multiple_choice', exercises, previous, true)
  assert.deepEqual(review.exercise_ids, [2])
  assert.notEqual(review.session_id, previous.session_id)
  assert.deepEqual(review.results, [])
  const fresh = newGuestSession('multiple_choice', exercises)
  saveGuestSession(1, fresh, store)
  assert.deepEqual(readGuestSessions(1, store), [fresh])
})
test('content signature catches changed order, answers and question text', () => {
  assert.notEqual(contentKey(exercises), contentKey([...exercises].reverse()))
  assert.notEqual(contentKey(exercises), contentKey([{ ...exercises[0], correct_answer: 'ج' }, exercises[1]]))
  assert.notEqual(contentKey(exercises), contentKey([{ ...exercises[0], question_ar: 'تعديل' }, exercises[1]]))
})
test('corrupt checkpoints and unavailable storage fail safely without touching auth', () => {
  const store = memory()
  store.setItem('token', 'keep')
  store.setItem('arabiq:guest-practice:v1:1', '{broken')
  assert.deepEqual(readGuestSessions(1, store), [])
  assert.equal(saveGuestSession(1, {}, null), false)
  const session = { ...newGuestSession('multiple_choice', exercises), current_index: 20 }
  store.setItem('arabiq:guest-practice:v1:1', JSON.stringify({ multiple_choice: session }))
  assert.deepEqual(readGuestSessions(1, store), [])
  assert.equal(store.getItem('token'), 'keep')
})
