import { useEffect, useState } from 'react'

const base = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')
export const TOKEN_KEY = 'takip-account-token'

export async function request(path, token, { method = 'GET', body, signal } = {}) {
  const headers = {}
  if (token) headers.Authorization = `Bearer ${token}`
  if (body) headers['Content-Type'] = body instanceof URLSearchParams
    ? 'application/x-www-form-urlencoded' : 'application/json'
  const response = await fetch(`${base}/api${path}`, {
    method, headers, signal, body: body instanceof URLSearchParams ? body : body ? JSON.stringify(body) : undefined,
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    if (response.status === 401 && token) window.dispatchEvent(new Event('takip-session-expired'))
    const message = typeof data.detail === 'string' ? data.detail : `HTTP ${response.status}`
    throw new Error(message)
  }
  return data
}

export function useResource(path, token, revision = 0) {
  const [result, setResult] = useState(null)
  const key = `${path}:${revision}:${token}`
  useEffect(() => {
    if (!path || !token) return
    const controller = new AbortController()
    request(path, token, { signal: controller.signal }).then(
      data => { if (!controller.signal.aborted) setResult({ key, data }) },
      error => { if (!controller.signal.aborted) setResult({ key, error: error.message }) },
    )
    return () => controller.abort()
  }, [path, token, key])
  return result?.key === key ? result : { loading: Boolean(path && token) }
}
