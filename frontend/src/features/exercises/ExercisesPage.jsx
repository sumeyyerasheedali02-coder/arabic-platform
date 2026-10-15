import { useMemo, useState } from 'react'
import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import { useAuth } from '../../auth/useAuth'
import ErrorState from '../../components/ErrorState'
import { CenteredSpinner } from '../../components/Spinner'
import { useProgress } from '../progress/useProgress'
import { useUnits } from '../units/useUnits'
import ExerciseCard from './ExerciseCard'
import SessionSummary from './SessionSummary'
import { FILTER_OPTIONS, matchesFilter } from './filters'
import { correctCount, scoresByLesson, successRate, totalPoints } from './session'
import { useLessonActivity } from '../activity/useLessonActivity'

const NO_EXERCISES = []
const newSession = (key) => ({ key, current: 0, results: [], done: false })

/** A practice session: the exercises of one unit, one at a time, optionally filtered by kind. */
export default function ExercisesPage() {
  const { token } = useAuth()
  const { units, selectedUnit, selectUnit, loading: loadingUnits, error: unitsError, reload: reloadUnits } = useUnits()
  const { reload: reloadProgress } = useProgress()
  const unitId = selectedUnit?.id
  const query = useApiData(
    unitId == null ? null : `exercises:${unitId}`,
    () => api.get(`/units/${unitId}/exercises`).then(r => r.data),
  )
  const [filter, setFilter] = useState('all')
  const isGuest = !token

  const allExercises = query.data ?? NO_EXERCISES
  const exercises = useMemo(
    () => allExercises.filter(ex => matchesFilter(ex, filter)),
    [allExercises, filter],
  )

  // A session belongs to one unit and one filter; changing either starts a new one
  const sessionKey = `${unitId}:${filter}`
  const [session, setSession] = useState(() => newSession(sessionKey))
  if (session.key !== sessionKey) setSession(newSession(sessionKey))
  const { current, results, done } = session.key === sessionKey ? session : newSession(sessionKey)
  useLessonActivity(!done && !query.loading ? exercises[current]?.lesson_id : null)

  const handleAnswer = (result) => setSession(s => ({ ...s, results: [...s.results, result] }))

  const finishSession = async () => {
    setSession(s => ({ ...s, done: true }))
    if (isGuest) return
    // One progress row per lesson the session touched, each with the points
    // earned on that lesson's exercises.
    try {
      await Promise.all(scoresByLesson(exercises, results).map(({ lessonId, score }) => (
        api.post('/me/progress/update', null, {
          params: { unit_id: unitId, lesson_id: lessonId, score, status: 'completed' },
        })
      )))
    } catch { /* the answers themselves are already saved; only the summary row is missing */ }
    reloadProgress()
  }

  const next = () => {
    if (current + 1 >= exercises.length) finishSession()
    else setSession(s => ({ ...s, current: s.current + 1 }))
  }

  const restart = () => setSession(newSession(sessionKey))

  if (loadingUnits) return <CenteredSpinner size={32} height={260} />
  if (unitsError && units.length === 0) return <ErrorState onRetry={reloadUnits} />

  const answered = results.length > current

  if (done) {
    return (
      <SessionSummary
        total={exercises.length} correctCount={correctCount(results)}
        pct={successRate(exercises, results)} totalPoints={totalPoints(results)}
        isGuest={isGuest} onRestart={restart}
      />
    )
  }

  return (
    <div style={{ maxWidth: 640, margin: '0 auto', padding: '28px 16px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
        <h1 style={{ fontSize: 17, fontWeight: 700, color: 'var(--navy)', margin: 0 }}>التمارين</h1>
        <select
          value={unitId || ''}
          onChange={e => selectUnit(units.find(u => u.id === Number(e.target.value)))}
          style={{
            fontSize: 13, background: '#fff', border: '1px solid var(--border)',
            borderRadius: 9, padding: '6px 12px', color: 'var(--navy)',
            outline: 'none', fontFamily: 'DM Sans, sans-serif', cursor: 'pointer',
          }}
        >
          {units.map(u => <option key={u.id} value={u.id}>{u.title_ar}</option>)}
        </select>
      </div>

      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 16 }}>
        {FILTER_OPTIONS.map(opt => (
          <button key={opt.value} onClick={() => setFilter(opt.value)} style={{
            padding: '4px 10px', borderRadius: 20, border: 'none', cursor: 'pointer',
            fontSize: 11, fontWeight: 600, fontFamily: 'DM Sans, sans-serif',
            background: filter === opt.value ? 'var(--navy)' : 'var(--cream)',
            color: filter === opt.value ? '#fff' : 'var(--navy)',
          }}>
            {opt.label} ({allExercises.filter(ex => matchesFilter(ex, opt.value)).length})
          </button>
        ))}
      </div>

      {query.loading ? (
        <CenteredSpinner size={28} height={160} />
      ) : query.error ? (
        <ErrorState compact onRetry={query.reload} />
      ) : exercises.length === 0 ? (
        <div style={{ background: '#fff', borderRadius: 14, padding: '48px 20px', textAlign: 'center', border: '1px solid var(--border)' }}>
          <div style={{ fontSize: 28, marginBottom: 10 }}>📝</div>
          <p style={{ color: 'var(--muted)', fontSize: 13 }}>لا توجد تمارين في هذه الوحدة</p>
        </div>
      ) : (
        <>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 18 }}>
            <div style={{ flex: 1, height: 4, background: 'var(--border)', borderRadius: 2, overflow: 'hidden' }}>
              <div style={{
                height: '100%', background: 'var(--gold)', borderRadius: 2,
                width: `${(current / exercises.length) * 100}%`, transition: 'width .4s',
              }} />
            </div>
            <span style={{ fontSize: 12, color: 'var(--muted)', flexShrink: 0 }}>{current + 1} / {exercises.length}</span>
          </div>

          <ExerciseCard
            key={exercises[current].id}
            exercise={exercises[current]}
            onAnswer={handleAnswer}
            isGuest={isGuest}
          />

          {answered && (
            <button
              onClick={next}
              style={{
                marginTop: 14, width: '100%', padding: '12px',
                background: 'var(--navy)', color: '#fff', border: 'none',
                borderRadius: 10, fontWeight: 600, fontSize: 14, cursor: 'pointer',
                fontFamily: 'DM Sans, sans-serif', transition: 'opacity .15s',
              }}
            >
              {current + 1 >= exercises.length ? 'انهاء الجلسة' : 'التالي'}
            </button>
          )}
        </>
      )}
    </div>
  )
}
