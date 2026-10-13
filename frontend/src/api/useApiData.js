import { useCallback, useEffect, useRef, useState } from 'react'

/**
 * Load data for a view and keep track of its loading / error state.
 *
 *   key   says what is being loaded ("unit-content:3"); null = nothing to load yet
 *   load  () => Promise<data>
 *
 * Returns { data, error, loading, reload }:
 *   data     what was loaded for this key (kept on screen while `reload` runs)
 *   loading  true until the first answer for this key arrives
 *   error    set when the latest attempt failed
 *
 * An answer that arrives after `key` has changed is ignored, so a slow request
 * can never overwrite what the user moved on to.
 */
export function useApiData(key, load, { refreshOnFocus = false } = {}) {
  const [result, setResult] = useState({ key: null, request: null, data: null, error: null })
  const [attempt, setAttempt] = useState(0)
  const request = key == null ? null : `${key}|${attempt}`

  const loadRef = useRef(load)
  useEffect(() => { loadRef.current = load })

  useEffect(() => {
    if (request == null) return undefined
    let current = true
    loadRef.current().then(
      (data) => { if (current) setResult({ key, request, data, error: null }) },
      (error) => {
        if (current) setResult((prev) => ({ key, request, data: prev.key === key ? prev.data : null, error }))
      },
    )
    return () => { current = false }
  }, [key, request])

  const reload = useCallback(() => setAttempt((n) => n + 1), [])

  useEffect(() => {
    if (!refreshOnFocus || key == null) return undefined
    let lastRefresh = Date.now()
    function refresh() {
      if (document.visibilityState !== 'visible' || Date.now() - lastRefresh < 1000) return
      lastRefresh = Date.now()
      reload()
    }
    window.addEventListener('focus', refresh)
    document.addEventListener('visibilitychange', refresh)
    return () => {
      window.removeEventListener('focus', refresh)
      document.removeEventListener('visibilitychange', refresh)
    }
  }, [key, refreshOnFocus, reload])

  const sameKey = key != null && result.key === key
  const settled = request != null && result.request === request
  const data = sameKey ? result.data : null
  return {
    data,
    error: settled ? result.error : null,
    loading: request != null && !settled && data == null,
    reload,
  }
}
