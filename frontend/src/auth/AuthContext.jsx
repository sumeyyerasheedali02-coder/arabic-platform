import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
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
  const [checkedToken, setCheckedToken] = useState(null)
  const sessionRevision = useRef(0)
  const navigate = useNavigate()

  const login = useCallback((accessToken, studentData) => {
    sessionRevision.current += 1
    writeSession(accessToken, studentData)
    setSession({ token: accessToken, student: studentData })
    setCheckedToken(accessToken)
  }, [])

  const logout = useCallback(() => {
    sessionRevision.current += 1
    clearSession()
    setSession(LOGGED_OUT)
    setCheckedToken(null)
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
    const revision = sessionRevision.current
    api.get('/auth/me').then(({ data }) => {
      if (!current || revision !== sessionRevision.current) return
      const student = {
        id: data.student_id, name: data.name,
        is_teacher: !!data.is_teacher, class_section: data.class_section ?? null,
        role: data.role, is_admin: !!data.is_admin,
        student_number: data.student_number ?? null,
      }
      writeSession(token, student)
      setSession(prev => (prev.token === token ? { token, student } : prev))
      setCheckedToken(token)
    }).catch(() => {
      // An offline user can still browse using their stored account details.
      if (current && revision === sessionRevision.current) setCheckedToken(token)
    })
    return () => { current = false }
  }, [token])

  const value = useMemo(
    () => ({ student: session.student, token: session.token, login, logout,
      loading: !!session.token && checkedToken !== session.token }),
    [session, checkedToken, login, logout],
  )
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
