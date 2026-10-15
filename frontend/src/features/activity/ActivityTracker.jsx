import { useEffect } from 'react'
import { useAuth } from '../../auth/useAuth'
import { API_BASE_URL } from '../../api/config'
import { activeSlice } from './activeClock'

export default function ActivityTracker() {
  const { token, student } = useAuth()
  const isStudent = Boolean(token && student && !student.is_teacher && !student.is_admin)
  useEffect(() => {
    if (!isStudent) return
    let last = performance.now()
    let input = last
    let visible = document.visibilityState === 'visible'
    let focused = document.hasFocus()
    let session = { session_id: crypto.randomUUID(), active_ms: 0, lesson_id: null }
    const tick = () => {
      const now = performance.now()
      session.active_ms += activeSlice(last, now, input, visible, focused)
      last = now
    }
    const send = () => {
      tick()
      // Keepalive can finish on navigation/close; cumulative values tolerate
      // repeated deliveries and late responses. Failed sends retry next tick.
      void fetch(`${API_BASE_URL}/me/progress/activity`, {
        method: 'POST', keepalive: true,
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ ...session, active_ms: Math.floor(session.active_ms) }),
      }).catch(() => {})
    }
    const interact = () => { tick(); input = performance.now() }
    const visibility = () => {
      send()
      visible = document.visibilityState === 'visible'
      focused = document.hasFocus()
      last = performance.now()
      if (visible && focused) input = last
    }
    const focus = () => { tick(); focused = true; input = last }
    const blur = () => { send(); focused = false }
    const lesson = event => {
      send()
      session = { session_id: crypto.randomUUID(), active_ms: 0, lesson_id: event.detail }
      send()
    }
    const inputs = ['pointerdown', 'pointermove', 'keydown', 'scroll', 'touchstart']
    inputs.forEach(name => window.addEventListener(name, interact, { passive: true, capture: true }))
    document.addEventListener('visibilitychange', visibility)
    window.addEventListener('focus', focus)
    window.addEventListener('blur', blur)
    window.addEventListener('pagehide', send)
    window.addEventListener('arabiq:active-lesson', lesson)
    const timer = window.setInterval(tick, 1000)
    const saver = window.setInterval(send, 15_000)
    send()
    return () => {
      send()
      clearInterval(timer); clearInterval(saver)
      inputs.forEach(name => window.removeEventListener(name, interact, true))
      document.removeEventListener('visibilitychange', visibility)
      window.removeEventListener('focus', focus)
      window.removeEventListener('blur', blur)
      window.removeEventListener('pagehide', send)
      window.removeEventListener('arabiq:active-lesson', lesson)
    }
  }, [token, isStudent])
  return null
}
