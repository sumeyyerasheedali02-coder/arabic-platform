import test from 'node:test'
import assert from 'node:assert/strict'
import { activeSlice, formatStudyTime, IDLE_MS } from '../src/features/activity/activeClock.js'

test('counts elapsed active time and cuts off exactly at the idle boundary', () => {
  assert.equal(activeSlice(1000, 2234, 1000, true, true), 1234)
  assert.equal(activeSlice(IDLE_MS - 500, IDLE_MS + 500, 0, true, true), 500)
  assert.equal(activeSlice(IDLE_MS + 100, IDLE_MS + 1100, 0, true, true), 0)
})

test('hidden, unfocused and suspended pages never accrue time', () => {
  assert.equal(activeSlice(0, 1000, 0, false, true), 0)
  assert.equal(activeSlice(0, 1000, 0, true, false), 0)
  assert.equal(activeSlice(0, 60_000, 0, true, true), 0)
})

test('short sessions are visible in seconds instead of rounded down to zero minutes', () => {
  assert.equal(formatStudyTime(25), '0 د · 25 ث')
  assert.equal(formatStudyTime(3672), '1 س · 1 د · 12 ث')
})
