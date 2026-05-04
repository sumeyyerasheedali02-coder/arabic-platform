import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : '/api'

const api = axios.create({ baseURL: API_BASE })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const isAuthEndpoint = err.config?.url?.startsWith('/auth/')
    const hasToken = !!localStorage.getItem('token')
    // Only force-redirect to login if the user had a token (session expired), not for guests
    if (err.response?.status === 401 && !isAuthEndpoint && hasToken) {
      localStorage.removeItem('token')
      localStorage.removeItem('student')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api
