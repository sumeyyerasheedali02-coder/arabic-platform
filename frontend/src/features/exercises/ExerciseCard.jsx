import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { TYPE_LABELS } from './filters'

/** Selection is deliberate; a restored result never submits an answer again. */
export default function ExerciseCard({ exercise, isGuest, onSubmit, initialResult = null, initialAnswer = '', onBusyChange }) {
  const [input, setInput] = useState(initialAnswer)
  const [selected, setSelected] = useState(initialAnswer)
  const [result, setResult] = useState(initialResult)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [needsReload, setNeedsReload] = useState(false)
  const [hint, setHint] = useState(false)
  const lock = useRef(false)
  const feedback = useRef(null)
  useEffect(() => {
    if (result && window.matchMedia('(max-width: 600px)').matches) {
      feedback.current?.scrollIntoView({ block: 'nearest', behavior: 'instant' })
    }
  }, [result])
  const options = exercise.exercise_type === 'true_false' ? ['صَحِيح', 'خَطَأ']
    : Array.isArray(exercise.options) && exercise.options.length ? exercise.options : null
  const value = options ? selected : input.trim()

  async function submit(event) {
    event.preventDefault()
    if (lock.current || result || !value) return
    lock.current = true
    setSubmitting(true)
    onBusyChange(true)
    setError('')
    setNeedsReload(false)
    try { setResult(await onSubmit(value)) }
    catch (err) {
      setNeedsReload(err.response?.status === 409)
      setError(typeof err.response?.data?.detail === 'string' ? err.response.data.detail
        : 'تعذّر حفظ الإجابة. تحقق من الاتصال ثم أعد المحاولة؛ لم تُحتسب إجابة خاطئة.')
    } finally {
      lock.current = false
      setSubmitting(false)
      onBusyChange(false)
    }
  }

  return (
    <form className="practice-question" onSubmit={submit}>
      <div className="practice-question-body">
      <span className="practice-question-kind">{TYPE_LABELS[exercise.category] || TYPE_LABELS[exercise.exercise_type]}</span>
      <h2 dir="auto">{exercise.question_ar}</h2>
      {exercise.question_tr && <p className="practice-question-translation" lang="tr" dir="ltr">{exercise.question_tr}</p>}
      {!result && exercise.hint_ar && <div className="practice-hint"><button type="button" onClick={() => setHint(v => !v)} aria-expanded={hint}>{hint ? 'إخفاء التلميح' : 'أحتاج تلميحًا'}</button>{hint && <p>{exercise.hint_ar}</p>}</div>}
      {options ? (
        <fieldset className={`practice-options${options.every(option => option.length <= 45) ? ' practice-options-short' : ''}`} disabled={submitting || !!result}>
          <legend className="practice-sr-only">اختر الإجابة</legend>
          {options.map((option, index) => (
            <button key={index} type="button" aria-pressed={selected === option} className={`practice-option${selected === option ? ' is-selected' : ''}`} onClick={() => { setSelected(option); setError('') }}>
              <span className="practice-option-number" aria-hidden="true">{index + 1}</span><span dir="auto">{option}</span><span className="practice-option-mark" aria-hidden="true">{selected === option ? '✓' : ''}</span>
            </button>
          ))}
        </fieldset>
      ) : (
        <label className="practice-answer-label">إجابتك
          <input dir="auto" autoComplete="off" enterKeyHint="done" value={input} onChange={e => { setInput(e.target.value); setError('') }} disabled={submitting || !!result} placeholder="اكتب إجابتك، ويمكنك الكتابة دون تشكيل" />
        </label>
      )}
      {error && <div role="alert" className="practice-error">{error}{needsReload && <button className="practice-text-button" type="button" onClick={() => window.location.reload()}>تحديث التدريب</button>}</div>}
      {result && <div ref={feedback} className={`practice-feedback ${result.is_correct ? 'is-correct' : 'is-incorrect'}`} role="status">
        <strong>{result.is_correct ? '✓ إجابة صحيحة' : 'الإجابة تحتاج تصحيحًا'}</strong>
        {!result.is_correct && result.correct_answer && <p>الإجابة الصحيحة: <b dir="auto">{result.correct_answer}</b></p>}
        {result.explanation_ar && <p>{result.explanation_ar}</p>}
      </div>}
      {isGuest && result && <p className="practice-save-note">الجلسة محفوظة على هذا الجهاز. <Link to="/login">سجّل الدخول لحفظ النتائج في حسابك.</Link></p>}
      </div>
      {!result && <div className="practice-question-actions"><button className="practice-button practice-primary practice-confirm" type="submit" disabled={!value || submitting}>{submitting ? 'جارٍ حفظ الإجابة…' : 'تأكيد الإجابة'}</button></div>}
    </form>
  )
}
