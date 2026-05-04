import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [student, setStudent] = useState(null)
  const [token, setToken]     = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const savedToken   = localStorage.getItem('token')
    const savedStudent = localStorage.getItem('student')
    if (savedToken && savedStudent) {
      setToken(savedToken)
      setStudent(JSON.parse(savedStudent))
    }
    setLoading(false)
  }, [])

  const login = (accessToken, studentData) => {
    localStorage.setItem('token',   accessToken)
    localStorage.setItem('student', JSON.stringify(studentData))
    setToken(accessToken)
    setStudent(studentData)
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('student')
    setToken(null)
    setStudent(null)
  }

  return (
    <AuthContext.Provider value={{ student, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
