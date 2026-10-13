import { useCallback, useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api, { setSessionRejectedHandler } from '../api/client'
import { clearSession, readSession, writeSession } from './session'
import { AuthContext } from './useAuth'

const LOGGED_OUT = { token: null, student: null }

/**
 * Holds the login for the whole app. Must be rendered inside the router: when
 * the server rejects a stored login, the student is sent to the login page.
 */
export function AuthProvider({ children }) {
  // Read synchronously, so the first render already knows who is logged in
  const [session, setSession] = useState(() => readSession() ?? LOGGED_OUT)
  const navigate = useNavigate()

  const login = useCallback((accessToken, studentData) => {
    writeSession(accessToken, studentData)
    setSession({ token: accessToken, student: studentData })
  }, [])

  const logout = useCallback(() => {
    clearSession()
    setSession(LOGGED_OUT)
  }, [])

  // The stored login was valid when it was saved; the server may have stopped
  // accepting it since (expired, signing key changed, account removed).
  useEffect(() => {
    setSessionRejectedHandler(() => {
      logout()
      navigate('/login', { state: { sessionExpired: true } })
    })
    return () => setSessionRejectedHandler(null)
  }, [logout, navigate])

  // Check a restored login once with the server and pick up changes to the
  // account (name, teacher rights). A rejection is handled by the handler above.
  const { token } = session
  useEffect(() => {
    if (!token) return undefined
    let current = true
    api.get('/auth/me').then(({ data }) => {
      if (!current) return
      const student = { id: data.student_id, name: data.name, is_teacher: !!data.is_teacher }
      writeSession(token, student)
      setSession(prev => (prev.token === token ? { token, student } : prev))
    }).catch(() => { /* offline or rejected: nothing to update */ })
    return () => { current = false }
  }, [token])

  const value = useMemo(
    // `loading` is kept for callers that wait for the login to be known; it is
    // known from the first render now.
    () => ({ student: session.student, token: session.token, login, logout, loading: false }),
    [session, login, logout],
  )
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
