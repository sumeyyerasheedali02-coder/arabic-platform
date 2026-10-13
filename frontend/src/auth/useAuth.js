import { createContext, useContext } from 'react'

export const AuthContext = createContext(null)

/** { student, token, login, logout, loading } */
export const useAuth = () => useContext(AuthContext)
