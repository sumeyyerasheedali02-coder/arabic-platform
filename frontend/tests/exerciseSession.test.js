import assert from 'node:assert/strict'
import { test } from 'node:test'
import { correctCount, scoresByLesson, successRate, totalPoints } from '../src/features/exercises/session.js'

const exercises = [
  { id: 1, lesson_id: 20, points: 10 },   // vocabulary lesson
  { id: 2, lesson_id: 20, points: 5 },
  { id: 3, lesson_id: 10, points: 10 },   // dialogue lesson
  { id: 4, lesson_id: 30, points: 15 },   // grammar lesson
  { id: 5, lesson_id: null, points: 10 }, // not attached to a lesson
]
const right = (points) => ({ is_correct: true, points_earned: points })
const wrong = { is_correct: false, points_earned: 0 }

test('success rate weighs exercises by their points', () => {
  assert.equal(successRate(exercises, [right(10), wrong, right(10), right(15), wrong]), 70)
  assert.equal(successRate(exercises, []), 0)
})

test('a guest who answers everything correctly gets 100%, not 0%', () => {
  const guest = { is_correct: true, points_earned: 0 }
  assert.equal(successRate(exercises, [guest, guest, guest, guest, guest]), 100)
})

test('only answered exercises count towards the rate', () => {
  assert.equal(successRate(exercises, [right(10), wrong]), 67)
})

test('points are attributed to the lesson each exercise belongs to', () => {
  const results = [right(10), right(5), wrong, right(15), right(10)]
  assert.deepEqual(scoresByLesson(exercises, results), [
    { lessonId: 20, score: 15 },
    { lessonId: 10, score: 0 },
    { lessonId: 30, score: 15 },
  ])
})

test('a lesson that was not reached is not reported', () => {
  assert.deepEqual(scoresByLesson(exercises, [right(10)]), [{ lessonId: 20, score: 10 }])
})

test('totals', () => {
  const results = [right(10), wrong, right(10)]
  assert.equal(totalPoints(results), 20)
  assert.equal(correctCount(results), 2)
})
