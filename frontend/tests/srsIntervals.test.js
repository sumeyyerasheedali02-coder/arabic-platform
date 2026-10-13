import assert from 'node:assert/strict'
import { test } from 'node:test'
import { afterDays, ratingLabel } from '../src/features/srs/intervals.js'

test('days are worded by Arabic number rules', () => {
  assert.equal(afterDays(1), 'بعد يوم واحد')
  assert.equal(afterDays(2), 'بعد يومين')
  assert.equal(afterDays(3), 'بعد 3 أيام')
  assert.equal(afterDays(6), 'بعد 6 أيام')
  assert.equal(afterDays(10), 'بعد 10 أيام')
  assert.equal(afterDays(11), 'بعد 11 يوماً')
  assert.equal(afterDays(15), 'بعد 15 يوماً')
})

test('nothing is shown when the interval is unknown', () => {
  assert.equal(afterDays(undefined), '')
  assert.equal(afterDays(0), '')
  assert.equal(ratingLabel({}, 4), '')
  assert.equal(ratingLabel(undefined, 4), '')
})

test('each rating shows the interval the server computed for it', () => {
  // second review of a card: failing brings it back tomorrow, passing in six days
  const card = { next_interval_days: { 0: 1, 1: 1, 2: 1, 3: 6, 4: 6, 5: 6 } }
  assert.equal(ratingLabel(card, 1), 'بعد يوم واحد')
  assert.equal(ratingLabel(card, 3), 'بعد 6 أيام')
  assert.equal(ratingLabel(card, 5), 'بعد 6 أيام')
})
