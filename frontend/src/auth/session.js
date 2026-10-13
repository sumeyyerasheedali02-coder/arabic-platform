// The stored login: a JWT plus the account it belongs to, in localStorage.
// Pure functions (the storage is a parameter) so they can be tested with Node.

const TOKEN_KEY = 'token'
const STUDENT_KEY = 'student'

const browserStorage = () => (typeof localStorage === 'undefined' ? null : localStorage)

/** Expiry time of a JWT in milliseconds, or null when it cannot be read. */
export function tokenExpiry(token) {
  try {
    const payload = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
    const { exp } = JSON.parse(atob(payload))
    return typeof exp === 'number' ? exp * 1000 : null
  } catch {
    return null
  }
}

/** True when the token is unreadable or past its expiry. The server has the final say. */
export function isTokenExpired(token, now = Date.now()) {
  const expiry = tokenExpiry(token)
  return expiry == null || expiry <= now
}

export function clearSession(storage = browserStorage()) {
  storage?.removeItem(TOKEN_KEY)
  storage?.removeItem(STUDENT_KEY)
}

export function writeSession(token, student, storage = browserStorage()) {
  storage?.setItem(TOKEN_KEY, token)
  storage?.setItem(STUDENT_KEY, JSON.stringify(student))
}

/**
 * The stored login as { token, student }, or null.
 * Anything incomplete, unreadable or expired is removed, so the app never
 * starts half logged in (a token without an account, or the other way round).
 */
export function readSession(storage = browserStorage(), now = Date.now()) {
  if (!storage) return null
  try {
    const token = storage.getItem(TOKEN_KEY)
    const student = JSON.parse(storage.getItem(STUDENT_KEY) || 'null')
    if (token && student && typeof student === 'object' && student.name && !isTokenExpired(token, now)) {
      return { token, student }
    }
  } catch { /* unreadable: treated as logged out below */ }
  clearSession(storage)
  return null
}

export function storedToken(storage = browserStorage()) {
  return storage?.getItem(TOKEN_KEY) || null
}
