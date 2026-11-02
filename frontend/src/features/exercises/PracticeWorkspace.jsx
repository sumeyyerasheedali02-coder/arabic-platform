import { useEffect, useRef, useState } from 'react'
import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import ErrorState from '../../components/ErrorState'
import { CenteredSpinner } from '../../components/Spinner'
import { useProgress } from '../progress/useProgress'
import { useLessonActivity } from '../activity/useLessonActivity'
import ExerciseCard from './ExerciseCard'
import SessionSummary from './SessionSummary'
import { FILTER_OPTIONS, matchesFilter } from './filters'
import { isCorrectAnswer } from './answers'
import { correctCount, successRate, totalPoints } from './session'
import { contentKey, newGuestSession, readGuestSessions, saveGuestSession } from './practiceStorage'

const DESCRIPTIONS = {
  multiple_choice: 'اختر الإجابة المناسبة', fill_blank: 'أكمل الجملة بالكلمة الصحيحة', true_false: 'ميّز بين الصحيح والخطأ',
  translate_ar_tr: 'تدرّب بين العربية والتركية', match: 'اربط الكلمات بمعانيها', synonym: 'اكتشف الكلمات المتشابهة',
  antonym: 'تعلّم الكلمات المتضادة', plural: 'انتقل من المفرد إلى الجمع', comprehension: 'اقرأ ثم أجب',
  word_order: 'رتّب الكلمات لبناء جملة', form_sentence: 'كوّن جملة صحيحة', respond: 'عبّر بإجابة قصيرة',
}

const TYPE_ICONS = {
  multiple_choice: <><rect x="3" y="3" width="18" height="18" rx="4" /><path d="m7 12 3 3 7-7" /></>,
  fill_blank: <><path d="M4 6h16M4 12h5m6 0h5M4 18h16M11 10v4m2-4v4" /></>,
  true_false: <><path d="m3 7 3 3 5-6m4 11 6 6m0-6-6 6M3 18h5M16 6h5" /></>,
  translate_ar_tr: <><path d="M3 5h12M8 3v2M5 5c1 5 4 8 8 10M13 5c-1 5-5 8-10 11M14 21l4-10 4 10M15 18h6" /></>,
  match: <><rect x="3" y="4" width="5" height="5" rx="1" /><rect x="16" y="15" width="5" height="5" rx="1" /><path d="M8 6h6a4 4 0 0 1 4 4v5M3 17h5m8-11h5" /></>,
  synonym: <><path d="M5 8h14m-3-3 3 3-3 3M19 16H5m3-3-3 3 3 3" /></>,
  antonym: <><path d="M4 8h7m-4-3-3 3 3 3M20 16h-7m4-3 3 3-3 3" /></>,
  plural: <><circle cx="9" cy="8" r="3" /><path d="M3 21v-2a6 6 0 0 1 12 0v2M16 5a3 3 0 0 1 0 6m2 4a5 5 0 0 1 3 4v2" /></>,
  comprehension: <><path d="M12 5c-3-2-6-2-9-1v15c3-1 6-1 9 1m0-15c3-2 6-2 9-1v15c-3-1-6-1-9 1V5" /></>,
  word_order: <><rect x="3" y="4" width="7" height="6" rx="1" /><rect x="14" y="4" width="7" height="6" rx="1" /><path d="M3 16h18M3 20h12" /></>,
}
function PracticeTypeIcon({ kind }) {
  return <svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{TYPE_ICONS[kind] ?? TYPE_ICONS.word_order}</svg>
}

function RestartDialog({ onCancel, onConfirm, busy }) {
  const dialog = useRef(null)
  useEffect(() => { dialog.current.showModal() }, [])
  return <dialog ref={dialog} className="practice-dialog" aria-labelledby="practice-restart-title" onCancel={onCancel}>
    <h2 id="practice-restart-title">البدء من البداية؟</h2>
    <p>سيبدأ هذا التدريب من السؤال الأول. تبقى إجاباتك السابقة في سجلك.</p>
    <div><button className="practice-button practice-primary" onClick={onConfirm} disabled={busy}>ابدأ من البداية</button><button className="practice-button practice-secondary" onClick={onCancel} disabled={busy}>إلغاء</button></div>
  </dialog>
}

export default function PracticeWorkspace({ unit, allExercises, isGuest }) {
  const { reload: reloadProgress } = useProgress()
  const savedQuery = useApiData(isGuest ? null : `practice:${unit.id}`, () => api.get(`/me/practice/${unit.id}`).then(r => r.data), { refreshOnFocus: true })
  const [guestSessions] = useState(() => isGuest ? readGuestSessions(unit.id) : [])
  const [overrides, setOverrides] = useState({})
  const [active, setActive] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [needsReload, setNeedsReload] = useState(false)
  const [saveWarning, setSaveWarning] = useState(false)
  const [restartKey, setRestartKey] = useState(null)
  const operation = useRef(false)
  const skills = FILTER_OPTIONS.map(option => ({ ...option, exercises: allExercises.filter(ex => matchesFilter(ex, option.value)) })).filter(skill => skill.exercises.length)
  const skillMap = new Map(skills.map(skill => [skill.value, skill]))
  const sessions = skills.map(skill => {
    const saved = overrides[skill.value] ?? (isGuest ? guestSessions : savedQuery.data ?? []).find(s => s.filter_key === skill.value)
    return saved && { ...saved, stale: saved.stale || (isGuest && saved.content_key !== contentKey(skill.exercises)) }
  }).filter(Boolean)
  const byFilter = new Map(sessions.map(session => [session.filter_key, session]))
  const latest = sessions.filter(session => !session.completed && !session.stale)
    .sort((a, b) => (b.updated_at ?? '').localeCompare(a.updated_at ?? ''))[0]
  const activeSkill = active ? skillMap.get(active.filter_key) : null
  const exercises = active ? active.exercise_ids.map(id => allExercises.find(ex => ex.id === id)).filter(Boolean) : []
  const exercise = active && !active.completed ? exercises[active.current_index] : null
  useLessonActivity(exercise?.lesson_id)

  function remember(session) {
    setOverrides(previous => ({ ...previous, [session.filter_key]: session }))
    if (isGuest && !saveGuestSession(unit.id, session)) setSaveWarning(true)
    setActive(session)
  }

  async function start(key, mode = 'resume') {
    if (operation.current) return
    operation.current = true
    setBusy(true)
    setError('')
    setNeedsReload(false)
    try {
      const previous = byFilter.get(key)
      const session = isGuest
        ? mode === 'resume' && previous && !previous.stale ? previous
          : newGuestSession(key, skillMap.get(key).exercises, previous, mode === 'mistakes')
        : (await api.post(`/me/practice/${unit.id}/${key}`, { restart: mode === 'restart', mistakes_only: mode === 'mistakes' })).data
      remember(session)
      setRestartKey(null)
    } catch (err) { setNeedsReload(err.response?.status === 409); setError(typeof err.response?.data?.detail === 'string' ? err.response.data.detail : 'تعذّر فتح التدريب. تحقق من الاتصال وأعد المحاولة.') }
    finally { operation.current = false; setBusy(false) }
  }

  async function submit(value) {
    let result
    if (isGuest) result = { is_correct: isCorrectAnswer(value, exercise.correct_answer), correct_answer: exercise.correct_answer, explanation_ar: null, points_earned: 0 }
    else result = (await api.post('/exercises/submit', { exercise_id: exercise.id, student_answer: value,
      practice_session_id: active.session_id, practice_filter: active.filter_key })).data
    remember({ ...active, results: [...active.results, { ...result, exercise_id: exercise.id, student_answer: value }], updated_at: new Date().toISOString() })
    return result
  }

  async function next() {
    if (operation.current) return
    operation.current = true
    setBusy(true)
    setError('')
    setNeedsReload(false)
    try {
      const index = active.current_index + 1
      const session = isGuest ? { ...active, current_index: index, completed: index === exercises.length, updated_at: new Date().toISOString() }
        : (await api.post(`/me/practice/${unit.id}/${active.filter_key}/advance`, { session_id: active.session_id, index: active.current_index })).data
      remember(session)
      if (session.completed && !isGuest) reloadProgress()
    } catch (err) { setNeedsReload(err.response?.status === 409); setError(typeof err.response?.data?.detail === 'string' ? err.response.data.detail : 'تعذّر الانتقال. إجابتك محفوظة؛ أعد المحاولة.') }
    finally { operation.current = false; setBusy(false) }
  }

  function back() { setActive(null); setError(''); savedQuery.reload() }
  if (!isGuest && savedQuery.loading) return <CenteredSpinner size={28} height={180} />
  if (!isGuest && savedQuery.error && !savedQuery.data && !active) return <ErrorState onRetry={savedQuery.reload} />

  return <>
    {restartKey && <RestartDialog busy={busy} onCancel={() => setRestartKey(null)} onConfirm={() => start(restartKey, 'restart')} />}
    {saveWarning && <p className="practice-error" role="alert">تعذّر الحفظ على هذا الجهاز. قد تضيع جلسة الضيف عند إغلاق الصفحة.</p>}
    {error && <div className="practice-error" role="alert">{error}{needsReload && <button className="practice-text-button" onClick={() => window.location.reload()}>تحديث التدريب</button>}</div>}
    <div className="practice-layout">
      {skills.length > 0 && <nav className="practice-type-list" aria-label="أنواع التدريب">
        <div className="practice-types-heading"><span>نوع التدريب <small>{skills.length}</small></span></div>
        <div className="practice-types-grid">
        {skills.map(skill => {
          const saved = byFilter.get(skill.value)
          const answered = saved && !saved.stale ? saved.results.length : 0
          const count = saved && !saved.stale ? saved.exercise_ids.length : skill.exercises.length
          return <button key={skill.value} className={`practice-type${active?.filter_key === skill.value ? ' is-active' : ''}`}
            aria-current={active?.filter_key === skill.value ? 'true' : undefined} disabled={busy}
            onClick={() => saved?.stale ? setRestartKey(skill.value) : start(skill.value)}>
            <span className="practice-type-icon"><PracticeTypeIcon kind={skill.value} /></span>
            <span className="practice-type-label">{skill.label}</span>
            <span className="practice-type-meta">{saved?.completed && !saved.stale ? '✓ تم التدريب' : answered ? <bdi dir="ltr">{answered} / {count}</bdi> : `${count} سؤال`}</span>
            <span className="practice-type-track" aria-hidden="true"><span style={{ width: `${count ? Math.min(100, answered / count * 100) : 0}%` }} /></span>
          </button>
        })}
        </div>
      </nav>}
      <div className="practice-main">
    {active ? <div className="practice-session">
      <div className="practice-session-nav"><span>{activeSkill?.label}</span><button className="practice-text-button" onClick={() => setRestartKey(active.filter_key)} disabled={busy}>من البداية</button></div>
      {active.completed ? <SessionSummary total={exercises.length} correctCount={correctCount(active.results)} pct={successRate(exercises, active.results)} totalPoints={totalPoints(active.results)} isGuest={isGuest} busy={busy}
        onRestart={() => setRestartKey(active.filter_key)} onMistakes={() => start(active.filter_key, 'mistakes')} onBack={back} />
        : exercise ? <>
          <div className="practice-session-progress"><span>السؤال {active.current_index + 1} من {exercises.length}</span><span>{active.results.length} إجابات محفوظة</span>
            <div role="progressbar" aria-label="تقدم التدريب" aria-valuemin={0} aria-valuemax={exercises.length} aria-valuenow={active.results.length}><span style={{ width: `${active.results.length / exercises.length * 100}%` }} /></div>
          </div>
          <ExerciseCard key={`${active.session_id}:${exercise.id}`} exercise={exercise} isGuest={isGuest} onSubmit={submit} onBusyChange={setBusy}
            initialResult={active.results[active.current_index] ?? null} initialAnswer={active.results[active.current_index]?.student_answer ?? ''} />
          {active.results.length > active.current_index && <button className="practice-button practice-primary practice-next" onClick={next} disabled={busy}>{active.current_index + 1 === exercises.length ? 'عرض النتيجة' : 'السؤال التالي ←'}</button>}
          <p className="practice-save-note">{isGuest ? 'تُحفظ جلستك على هذا الجهاز.' : 'يُحفظ موضعك في حسابك بعد كل إجابة.'}</p>
        </> : <div className="practice-error">تغيّر محتوى الجلسة.<button className="practice-text-button" onClick={() => window.location.reload()}>تحديث التدريب</button></div>}
    </div> : <section className="practice-welcome">
      {skills.length ? <>
        <span className="practice-eyebrow">{latest ? 'أكمل من حيث وصلت' : 'خطوة جديدة في تعلّمك'}</span>
        <h2>{latest ? skillMap.get(latest.filter_key)?.label : 'تدرّب على لغتك'}</h2>
        <p>{latest ? `السؤال ${latest.current_index + 1} من ${latest.exercise_ids.length}` : 'اختر نوع التدريب، ثم أجب على مهل.'}</p>
        <div className="practice-welcome-detail">{latest ? DESCRIPTIONS[latest.filter_key] : `${skills.length} أنواع تدريب · ${allExercises.length} سؤال`}</div>
        <button className="practice-button practice-primary" onClick={() => start(latest?.filter_key ?? skills[0].value)} disabled={busy}>{latest ? 'متابعة التدريب ←' : 'ابدأ التدريب ←'}</button>
      </> : <><h2>لا توجد تدريبات لهذه الوحدة حاليًا</h2><p>اختر وحدة أخرى من القائمة.</p></>}
    </section>}
      </div>
    </div>
  </>
}
