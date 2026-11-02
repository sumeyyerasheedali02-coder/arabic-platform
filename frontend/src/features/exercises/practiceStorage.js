// Guest checkpoints stay on this device. Student checkpoints live on the server.
const KEY = 'arabiq:guest-practice:v1:'
const storage = () => { try { return window.localStorage } catch { return null } }

export const contentKey = exercises => JSON.stringify(exercises.map(ex => [
  ex.id, ex.lesson_id, ex.exercise_type, ex.category, ex.question_ar, ex.question_tr,
  ex.options, ex.correct_answer, ex.hint_ar, ex.hint_tr, ex.points,
]))

export function readGuestSessions(unitId, store = storage()) {
  try {
    const saved = JSON.parse(store?.getItem(KEY + unitId) || '{}')
    return Object.values(saved).filter(s => s && typeof s.filter_key === 'string'
      && typeof s.session_id === 'string' && Array.isArray(s.exercise_ids) && s.exercise_ids.length > 0
      && new Set(s.exercise_ids).size === s.exercise_ids.length
      && Number.isInteger(s.current_index) && s.current_index >= 0 && s.current_index <= s.exercise_ids.length
      && typeof s.completed === 'boolean' && s.completed === (s.current_index === s.exercise_ids.length)
      && Array.isArray(s.results) && s.results.length >= s.current_index
      && s.results.length <= Math.min(s.current_index + 1, s.exercise_ids.length)
      && s.results.every((r, i) => r && r.exercise_id === s.exercise_ids[i] && typeof r.is_correct === 'boolean'))
  } catch { return [] }
}

export function saveGuestSession(unitId, session, store = storage()) {
  try {
    if (!store) return false
    const sessions = Object.fromEntries(readGuestSessions(unitId, store).map(s => [s.filter_key, s]))
    store.setItem(KEY + unitId, JSON.stringify({ ...sessions, [session.filter_key]: session }))
    return true
  } catch { return false }
}

export function newGuestSession(filter, exercises, previous = null, mistakesOnly = false) {
  const wrong = new Set(previous?.results.filter(r => !r.is_correct).map(r => r.exercise_id) ?? [])
  return {
    session_id: crypto.randomUUID(), filter_key: filter,
    exercise_ids: exercises.filter(ex => !mistakesOnly || wrong.has(ex.id)).map(ex => ex.id),
    content_key: contentKey(exercises), results: [], current_index: 0, completed: false,
    updated_at: new Date().toISOString(), stale: false,
  }
}
