import assert from 'node:assert/strict'
import { test } from 'node:test'
import { clearSession, isTokenExpired, readSession, tokenExpiry, writeSession } from '../src/auth/session.js'

const NOW = Date.UTC(2026, 0, 15)

function fakeStorage(initial = {}) {
  const data = new Map(Object.entries(initial))
  return {
    getItem: (key) => (data.has(key) ? data.get(key) : null),
    setItem: (key, value) => data.set(key, String(value)),
    removeItem: (key) => data.delete(key),
    keys: () => [...data.keys()].sort(),
  }
}

// A JWT-shaped token; the signature is irrelevant here (only the server checks it).
function token(expiresInSeconds) {
  const encode = (obj) => Buffer.from(JSON.stringify(obj)).toString('base64url')
  const exp = Math.floor(NOW / 1000) + expiresInSeconds
  return `${encode({ alg: 'HS256', typ: 'JWT' })}.${encode({ sub: '7', exp })}.signature`
}

const student = { id: 7, name: 'Ayşe Yılmaz', is_teacher: false }

test('tokenExpiry reads the exp claim in milliseconds', () => {
  assert.equal(tokenExpiry(token(60)), NOW + 60_000)
  assert.equal(tokenExpiry('not-a-token'), null)
  assert.equal(tokenExpiry(''), null)
})

test('isTokenExpired treats unreadable tokens as expired', () => {
  assert.equal(isTokenExpired(token(60), NOW), false)
  assert.equal(isTokenExpired(token(-60), NOW), true)
  assert.equal(isTokenExpired('abc.def.ghi', NOW), true)
})

test('a written session is read back', () => {
  const storage = fakeStorage()
  writeSession(token(3600), student, storage)
  assert.deepEqual(readSession(storage, NOW), { token: token(3600), student })
})

test('an expired session is discarded', () => {
  const storage = fakeStorage({ token: token(-1), student: JSON.stringify(student) })
  assert.equal(readSession(storage, NOW), null)
  assert.deepEqual(storage.keys(), [])
})

test('corrupt account data does not throw and is discarded', () => {
  const storage = fakeStorage({ token: token(3600), student: '{not json' })
  assert.equal(readSession(storage, NOW), null)
  assert.deepEqual(storage.keys(), [])
})

test('half a session is not a session', () => {
  const tokenOnly = fakeStorage({ token: token(3600) })
  assert.equal(readSession(tokenOnly, NOW), null)
  assert.deepEqual(tokenOnly.keys(), [])

  const studentOnly = fakeStorage({ student: JSON.stringify(student) })
  assert.equal(readSession(studentOnly, NOW), null)
  assert.deepEqual(studentOnly.keys(), [])
})

test('clearSession leaves other stored values alone', () => {
  const storage = fakeStorage({ token: 'x', student: '{}', theme: 'dark' })
  clearSession(storage)
  assert.deepEqual(storage.keys(), ['theme'])
})

test('no storage (private mode, server rendering) means logged out', () => {
  assert.equal(readSession(null, NOW), null)
})
