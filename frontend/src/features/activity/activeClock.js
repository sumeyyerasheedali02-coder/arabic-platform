export const IDLE_MS = 90_000

// Measure elapsed monotonic time, never timer tick counts (background timers drift).
export function activeSlice(previous, now, lastInput, visible, focused) {
  if (!visible || !focused || now - previous > 5000) return 0
  return Math.max(0, Math.min(now, lastInput + IDLE_MS) - previous)
}

export function formatStudyTime(seconds = 0) {
  const value = Math.max(0, Math.floor(seconds))
  const hours = Math.floor(value / 3600)
  const minutes = Math.floor(value % 3600 / 60)
  const rest = value % 60
  return `${hours ? `${hours} س · ` : ''}${minutes} د · ${rest} ث`
}
