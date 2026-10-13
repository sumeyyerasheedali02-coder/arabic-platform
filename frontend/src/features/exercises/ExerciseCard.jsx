import { useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../../api/client'
import { isCorrectAnswer } from './answers'
import { TYPE_LABELS } from './filters'

const TRUE_FALSE_CHOICES = [['صَحِيح', '#15803d', '#dcfce7'], ['خَطَأ', '#b91c1c', '#fee2e2']]

/** One exercise: question, the input that fits its type, then the result. */
export default function ExerciseCard({ exercise, onAnswer, isGuest }) {
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
      // Guest: checked locally with the same rule as the server, nothing is saved
      const ok = isCorrectAnswer(value, exercise.correct_answer)
      setShowLoginHint(true)
      setResult({ is_correct: ok, correct_answer: exercise.correct_answer || '', points_earned: 0 })
      onAnswer({ is_correct: ok, points_earned: 0 })
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
              {TRUE_FALSE_CHOICES.map(([val, color, bg]) => (
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
