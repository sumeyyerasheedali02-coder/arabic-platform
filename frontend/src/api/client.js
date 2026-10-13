import axios from 'axios'
import { storedToken } from '../auth/session'
import { API_BASE_URL } from './config'

// Every request to the backend goes through this instance.
const api = axios.create({
  baseURL: API_BASE_URL,
})

api.interceptors.request.use((config) => {
  const token = storedToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

let onSessionRejected = null

/** Called when the server rejects the stored login (set by AuthProvider). */
export function setSessionRejectedHandler(handler) {
  onSessionRejected = handler
}

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const sentToken = Boolean(error.config?.headers?.Authorization)
    const isAuthCall = (error.config?.url || '').startsWith('/auth/') && !error.config.url.startsWith('/auth/me')
    // A wrong password on the login form is also a 401, but it is not an expired session.
    if (error.response?.status === 401 && sentToken && !isAuthCall) {
      onSessionRejected?.()
    }
    return Promise.reject(error)
  },
)

export default api
