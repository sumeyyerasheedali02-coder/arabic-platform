import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/client'
import { useAuth } from '../context/AuthContext'

const TYPE_LABELS = {
  multiple_choice: 'اختيار من متعدد',
  fill_blank:      'اكمل الفراغ',
  translate_ar_tr: 'ترجمة عربي - تركي',
  translate_tr_ar: 'ترجمة تركي - عربي',
  true_false:      'صح ام خطا',
  form_sentence:   'كون جملة',
  respond:         'اجب بالعربية',
  match:           'وصل المعاني',
}

function ExerciseCard({ exercise, onAnswer, isGuest }) {
  const [input, setInput]           = useState('')
  const [selected, setSelected]     = useState(null)
  const [result, setResult]         = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [showLoginHint, setShowLoginHint] = useState(false)

  const submit = async (answer) => {
    if (submitting || result) return
    const value = answer ?? input.trim()
    if (!value) return

    if (isGuest) {
      // Guest: check locally without saving to DB
      setShowLoginHint(true)
      setResult({ is_correct: false, correct_answer: exercise.correct_answer || '', points_earned: 0 })
      onAnswer({ is_correct: false, points_earned: 0 })
      return
    }

    setSubmitting(true)
    try {
      const res = await api.post('/exercises/submit', { exercise_id: exercise.id, student_answer: value })
      setResult(res.data)
      onAnswer(res.data)
    } catch {
      setResult({ is_correct: false, correct_answer: exercise.correct_answer || '', points_earned: 0 })
    } finally { setSubmitting(false) }
  }

  const options = Array.isArray(exercise.options) ? exercise.options : null

  return (
    <div style={{ background: '#fff', borderRadius: 16, border: '1px solid var(--border)', padding: 20 }}>
      <span style={{
        fontSize: 10, fontWeight: 700, color: 'var(--navy)',
        background: 'var(--cream)', border: '1px solid var(--border)',
        borderRadius: 20, padding: '3px 10px',
      }}>
        {TYPE_LABELS[exercise.exercise_type] || exercise.exercise_type}
      </span>

      <div style={{ marginTop: 16, marginBottom: 18 }}>
        <p style={{ fontSize: 16, fontWeight: 700, color: 'var(--navy)', lineHeight: 1.6, fontFamily: "'Amiri', serif" }}>
          {exercise.question_ar}
        </p>
        {exercise.question_tr && (
          <p style={{ fontSize: 12, color: 'var(--muted)', marginTop: 4 }} dir="ltr">{exercise.question_tr}</p>
        )}
        {!result && exercise.hint_ar && (
          <p style={{ fontSize: 12, color: '#92400e', background: '#fff7ed', border: '1px solid #fed7aa', borderRadius: 9, padding: '8px 12px', marginTop: 10 }}>
            تلميح: {exercise.hint_ar}
          </p>
        )}
      </div>

      {!result && (
        <>
          {exercise.exercise_type === 'multiple_choice' && options ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {options.map((opt, i) => (
                <button
                  key={i}
                  onClick={() => { setSelected(opt); submit(opt) }}
                  style={{
                    width: '100%', textAlign: 'right', padding: '11px 16px', borderRadius: 10,
                    border: `1px solid ${selected === opt ? 'var(--navy)' : 'var(--border)'}`,
                    background: selected === opt ? 'rgba(15,32,68,.06)' : '#fff',
                    color: 'var(--navy)', fontSize: 14, fontFamily: "'Amiri', serif",
                    cursor: 'pointer', transition: 'all .15s',
                  }}
                >
                  {opt}
                </button>
              ))}
            </div>
          ) : exercise.exercise_type === 'true_false' ? (
            <div style={{ display: 'flex', gap: 10 }}>
              {[['صَحِيح', '#15803d', '#dcfce7'], ['خَطَأ', '#b91c1c', '#fee2e2']].map(([val, color, bg]) => (
                <button key={val} onClick={() => submit(val)} style={{
                  flex: 1, padding: '11px', borderRadius: 10, border: `1px solid ${color}20`,
                  background: bg, color, fontWeight: 700, fontSize: 15, cursor: 'pointer',
                  fontFamily: "'Amiri', serif", transition: 'opacity .15s',
                }}>
                  {val}
                </button>
              ))}
            </div>
          ) : (
            <div style={{ display: 'flex', gap: 8 }}>
              <input
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && submit()}
                placeholder="اكتب بدون تشكيل..."
                style={{
                  flex: 1, padding: '10px 14px', borderRadius: 10,
                  border: '1px solid var(--border)', outline: 'none',
                  fontSize: 14, color: 'var(--navy)', background: 'var(--cream)',
                  fontFamily: 'DM Sans, sans-serif', transition: 'border-color .15s',
                }}
                disabled={submitting}
                onFocus={e => e.target.style.borderColor = 'var(--navy)'}
                onBlur={e => e.target.style.borderColor = 'var(--border)'}
              />
              <button
                onClick={() => submit()}
                disabled={!input.trim() || submitting}
                style={{
                  padding: '10px 20px', borderRadius: 10, border: 'none',
                  background: input.trim() ? 'var(--navy)' : 'var(--border)',
                  color: input.trim() ? '#fff' : 'var(--muted)',
                  fontWeight: 600, fontSize: 13, cursor: input.trim() ? 'pointer' : 'default',
                  fontFamily: 'DM Sans, sans-serif', transition: 'all .15s',
                }}
              >
                ارسال
              </button>
            </div>
          )}
        </>
      )}

      {result && (
        <div style={{
          borderRadius: 12, padding: '14px 16px', marginTop: 10,
          background: result.is_correct ? '#f0fdf4' : '#fef2f2',
          border: `1px solid ${result.is_correct ? '#bbf7d0' : '#fecaca'}`,
        }}>
          <div style={{ fontWeight: 700, fontSize: 14, color: result.is_correct ? '#15803d' : '#b91c1c', marginBottom: 4 }}>
            {result.is_correct ? `اجابة صحيحة! +${result.points_earned} نقطة` : 'اجابة خاطئة'}
          </div>
          {!result.is_correct && result.correct_answer && (
            <p style={{ fontSize: 13, color: 'var(--text)' }}>
              الاجابة الصحيحة:{' '}
              <span style={{ fontWeight: 700, fontFamily: "'Amiri', serif", fontSize: 16 }}>{result.correct_answer}</span>
            </p>
          )}
          {result.explanation_ar && (
            <p style={{ fontSize: 12, color: 'var(--muted)', marginTop: 4 }}>{result.explanation_ar}</p>
          )}
          {showLoginHint && (
            <div style={{ marginTop: 8, paddingTop: 8, borderTop: '1px solid rgba(0,0,0,.08)', fontSize: 12, color: 'var(--muted)' }}>
              سجّل الدخول لحفظ نقاطك —{' '}
              <Link to="/login" style={{ color: 'var(--navy)', textDecoration: 'underline' }}>تسجيل الدخول</Link>
            </div>
          )}
        </div>
      )}
    </div>
  )
}


const FILTER_OPTIONS = [
  { value: 'all',             label: 'الكل' },
  { value: 'multiple_choice', label: 'اختيار متعدد' },
  { value: 'fill_blank',      label: 'إكمال فراغ' },
  { value: 'true_false',      label: 'صح وخطأ' },
  { value: 'translate_ar_tr', label: 'ترجمة' },
  { value: 'match',           label: 'وصل' },
  { value: 'synonym',         label: 'مترادفات' },
  { value: 'antonym',         label: 'متعاكسات' },
  { value: 'plural',          label: 'الجمع' },
  { value: 'comprehension',   label: 'استيعاب قرائي' },
  { value: 'word_order',      label: 'ترتيب كلمات' },
]

function matchesFilter(exercise, filter) {
  if (filter === 'all') return true
  if (filter === 'synonym')      return exercise.hint_ar === 'مترادف'
  if (filter === 'antonym')      return exercise.hint_ar === 'ضد / متعاكس'
  if (filter === 'plural')       return exercise.hint_ar === 'جمع الكلمة'
  if (filter === 'comprehension') return exercise.hint_ar === 'استيعاب قرائي'
  if (filter === 'word_order')   return exercise.question_ar && exercise.question_ar.includes('رَتِّب')
  return exercise.exercise_type === filter
}

export default function Exercises() {
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

  if (loading) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 260 }}>
      <div style={{ width: 32, height: 32, border: '3px solid var(--border)', borderTopColor: 'var(--gold)', borderRadius: '50%', animation: 'spin .8s linear infinite' }} />
    </div>
  )

  const answered     = session.length > current
  const totalPoints  = session.reduce((s, r) => s + (r?.points_earned || 0), 0)
  const correctCount = session.filter(r => r?.is_correct).length
  const maxPoints    = exercises.slice(0, session.length).reduce((s, e) => s + (e.points || 10), 0)

  if (done) {
    const pct = maxPoints > 0 ? Math.round((totalPoints / maxPoints) * 100) : 0
    return (
      <div style={{ maxWidth: 440, margin: '0 auto', padding: '60px 16px', textAlign: 'center' }}>
        <div style={{ fontSize: 64, marginBottom: 16 }}>{pct >= 80 ? '🏆' : pct >= 50 ? '👏' : '💪'}</div>
        <h1 style={{ fontSize: 22, fontWeight: 700, color: 'var(--navy)', marginBottom: 8 }}>انتهت جلسة التمارين!</h1>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 10, margin: '24px 0' }}>
          {[['📝', exercises.length, 'تمرين'], ['✅', correctCount, 'صحيح'], ['📊', `${pct}%`, 'نجاح']].map(([icon, val, label]) => (
            <div key={label} style={{ background: '#fff', borderRadius: 14, padding: '14px 10px', border: '1px solid var(--border)' }}>
              <div style={{ fontSize: 22, marginBottom: 4 }}>{icon}</div>
              <div style={{ fontSize: 20, fontWeight: 700, color: 'var(--navy)' }}>{val}</div>
              <div style={{ fontSize: 11, color: 'var(--muted)' }}>{label}</div>
            </div>
          ))}
        </div>
        {isGuest && (
          <p style={{ fontSize: 12, color: 'var(--muted)', marginBottom: 12 }}>
            سجّل الدخول لحفظ نتائجك —{' '}
            <Link to="/login" style={{ color: 'var(--navy)', textDecoration: 'underline' }}>تسجيل الدخول</Link>
          </p>
        )}
        {!isGuest && (
          <p style={{ fontSize: 13, color: 'var(--muted)', marginBottom: 16 }}>
            مجموع النقاط: <span style={{ fontWeight: 700, color: 'var(--navy)' }}>{totalPoints}</span>
          </p>
        )}
        <button onClick={restart} style={{
          background: 'var(--navy)', color: '#fff', border: 'none', cursor: 'pointer',
          borderRadius: 10, padding: '11px 32px', fontWeight: 600, fontSize: 14,
          fontFamily: 'DM Sans, sans-serif',
        }}>
          حاول مرة اخرى
        </button>
      </div>
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
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 160 }}>
          <div style={{ width: 28, height: 28, border: '3px solid var(--border)', borderTopColor: 'var(--gold)', borderRadius: '50%', animation: 'spin .8s linear infinite' }} />
        </div>
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
