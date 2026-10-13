// Arithmetic of a practice session. `exercises` is the list being practised and
// `results[i]` is the outcome of `exercises[i]` ({ is_correct, points_earned }).

const pointsOf = (exercise) => exercise.points || 10

/**
 * Success rate in percent: points of the correctly answered exercises over
 * the points of all answered ones. Based on correctness, not on awarded
 * points, so it also works for guests (who are awarded none).
 */
export function successRate(exercises, results) {
  const answered = exercises.slice(0, results.length)
  const possible = answered.reduce((sum, exercise) => sum + pointsOf(exercise), 0)
  const right = answered.reduce(
    (sum, exercise, i) => sum + (results[i]?.is_correct ? pointsOf(exercise) : 0), 0)
  return possible > 0 ? Math.round((right / possible) * 100) : 0
}

/**
 * Points earned per lesson, as [{ lessonId, score }].
 * A unit's exercises belong to several lessons (dialogues, vocabulary,
 * grammar), so one session usually touches more than one.
 */
export function scoresByLesson(exercises, results) {
  const scores = new Map()
  exercises.slice(0, results.length).forEach((exercise, i) => {
    if (exercise.lesson_id == null) return
    const earned = results[i]?.points_earned || 0
    scores.set(exercise.lesson_id, (scores.get(exercise.lesson_id) || 0) + earned)
  })
  return [...scores].map(([lessonId, score]) => ({ lessonId, score }))
}

export const totalPoints = (results) => results.reduce((sum, r) => sum + (r?.points_earned || 0), 0)
export const correctCount = (results) => results.filter(r => r?.is_correct).length
