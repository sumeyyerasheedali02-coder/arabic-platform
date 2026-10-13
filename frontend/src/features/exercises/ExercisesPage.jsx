import { useEffect, useState } from 'react'
import api from '../../api/client'
import { useAuth } from '../../auth/useAuth'
import { CenteredSpinner } from '../../components/Spinner'
import ExerciseCard from './ExerciseCard'
import SessionSummary from './SessionSummary'
import { FILTER_OPTIONS, matchesFilter } from './filters'

/** A practice session: the exercises of one unit, one at a time, optionally filtered by kind. */
export default function ExercisesPage() {
  const { token }                     = useAuth()
  const [units, setUnits]             = useState([])
  const [selectedUnit, setSelectedUnit] = useState(null)
  const [allExercises, setAllExercises] = useState([])
  const [exercises, setExercises]       = useState([])
  const [filter, setFilter]             = useState('all')
  const [current, setCurrent]         = useState(0)
  const [session, setSession]         = useState([])
  const [done, setDone]               = useState(false)
  const [loading, setLoading]         = useState(true)
  const [loadingEx, setLoadingEx]     = useState(false)
  const isGuest = !token

  useEffect(() => {
    api.get('/units').then(r => {
      setUnits(r.data)
      if (r.data.length > 0) setSelectedUnit(r.data[0])
    }).finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (!selectedUnit) return
    setLoadingEx(true)
    setExercises([])
    setCurrent(0)
    setSession([])
    setDone(false)
    api.get(`/units/${selectedUnit.id}/exercises`)
      .then(r => { setAllExercises(r.data); setExercises(r.data) })
      .finally(() => setLoadingEx(false))
  }, [selectedUnit])

  useEffect(() => {
    const filtered = allExercises.filter(ex => matchesFilter(ex, filter))
    setExercises(filtered)
    setCurrent(0)
    setSession([])
    setDone(false)
  }, [filter, allExercises])

  const handleAnswer = (result) => setSession(s => [...s, result])

  const next = async () => {
    if (current + 1 >= exercises.length) await finishSession()
    else setCurrent(c => c + 1)
  }

  const finishSession = async () => {
    setDone(true)
    if (!isGuest) {
      const totalScore = session.reduce((s, r) => s + (r?.points_earned || 0), 0)
      const firstEx    = exercises[0]
      if (firstEx?.lesson_id && selectedUnit) {
        try {
          await api.post(`/me/progress/update?unit_id=${selectedUnit.id}&lesson_id=${firstEx.lesson_id}&score=${totalScore}&status=completed`)
        } catch { /* non-critical */ }
      }
    }
  }

  const restart = () => { setCurrent(0); setSession([]); setDone(false) }

  if (loading) return <CenteredSpinner size={32} height={260} />

  const answered     = session.length > current
  const totalPoints  = session.reduce((s, r) => s + (r?.points_earned || 0), 0)
  const correctCount = session.filter(r => r?.is_correct).length
  const maxPoints    = exercises.slice(0, session.length).reduce((s, e) => s + (e.points || 10), 0)

  if (done) {
    const pct = maxPoints > 0 ? Math.round((totalPoints / maxPoints) * 100) : 0
    return (
      <SessionSummary
        total={exercises.length} correctCount={correctCount} pct={pct}
        totalPoints={totalPoints} isGuest={isGuest} onRestart={restart}
      />
    )
  }

  return (
    <div style={{ maxWidth: 640, margin: '0 auto', padding: '28px 16px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
        <h1 style={{ fontSize: 17, fontWeight: 700, color: 'var(--navy)', margin: 0 }}>التمارين</h1>
        <select
          value={selectedUnit?.id || ''}
          onChange={e => setSelectedUnit(units.find(u => u.id === Number(e.target.value)))}
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

      {loadingEx ? (
        <CenteredSpinner size={28} height={160} />
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
