import { Link, useSearchParams } from 'react-router-dom'
import { useState } from 'react'
import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import { CenteredSpinner } from '../../components/Spinner'
import LessonsPage from '../lessons/LessonsPage'
import { useUnits } from '../units/useUnits'
import { FILTER_OPTIONS, matchesFilter, TYPE_LABELS } from '../exercises/filters'
import { StaffMessage } from '../teacher/StaffUi'
import { apiError } from '../teacher/staffFormat'

function ExerciseLibrary() {
  const { units, selectedUnit, selectUnit, loading, error, reload } = useUnits()
  const unitId = selectedUnit?.id
  const [filter, setFilter] = useState('all')
  const [search, setSearch] = useState('')
  const query = useApiData(unitId ? `library-exercises:${unitId}` : null,
    () => api.get(`/units/${unitId}/exercises`).then(r => r.data))
  if (loading || query.loading) return <CenteredSpinner size={30} height={220} />
  if (error || query.error) return <div className="staff-page"><StaffMessage error={apiError(error || query.error)}
    onRetry={() => { reload(); query.reload() }} /></div>
  const exercises = (query.data ?? []).filter(e => matchesFilter(e, filter)
    && `${e.question_ar} ${e.question_tr || ''}`.includes(search.trim()))
  return <div className="staff-page">
    <section className="staff-panel">
      <div className="staff-toolbar"><h2>{selectedUnit?.title_ar || 'التمارين'}</h2>
        <label className="staff-library-unit-select">الوحدة
          <select value={unitId ?? ''} onChange={e => selectUnit(units.find(u => u.id === Number(e.target.value)))}>
            {units.map(u => <option key={u.id} value={u.id}>{u.unit_number}. {u.title_ar}</option>)}
          </select>
        </label>
        <input aria-label="البحث في التمارين" className="staff-search" placeholder="ابحث في نص السؤال"
          value={search} onChange={e => setSearch(e.target.value)} />
        <select aria-label="نوع التمرين" value={filter} onChange={e => setFilter(e.target.value)}>
          {FILTER_OPTIONS.map(f => <option key={f.value} value={f.value}>{f.label}</option>)}
        </select>
      </div>
      <p className="staff-intro">{exercises.length} تمرينًا · معاينة للتحضير والشرح.</p>
      {exercises.map(e => <article className="staff-exercise-preview" key={e.id}>
        <span className="staff-badge inactive">{TYPE_LABELS[e.exercise_type] || e.exercise_type}</span>
        <h3>{e.question_ar}</h3>
        {e.question_tr && <p dir="ltr">{e.question_tr}</p>}
        {Array.isArray(e.options) && <ul>{e.options.map((o,i) => <li key={i}>{String(o)}</li>)}</ul>}
        {e.hint_ar && <p>تلميح: {e.hint_ar}</p>}
        <details><summary>عرض الإجابة الصحيحة</summary><p>{e.correct_answer || 'غير مدخلة'}</p></details>
      </article>)}
      {!exercises.length && <p className="staff-empty">لا توجد تمارين مطابقة.</p>}
    </section>
  </div>
}

export default function ContentLibraryPage() {
  const [params] = useSearchParams()
  const exercises = params.get('tab') === 'exercises'
  return <div className="staff-library" dir="rtl">
    <div className="staff-page staff-library-heading">
      <h1>المحتوى التعليمي</h1>
      <p className="staff-intro">معاينة الدروس والمفردات والتمارين للتحضير والشرح.</p>
      <nav className="staff-tabs" aria-label="أنواع المحتوى">
        <Link className="staff-button" to="/content" aria-current={!exercises ? 'page' : undefined}>الدروس والمفردات</Link>
        <Link className="staff-button" to="/content?tab=exercises" aria-current={exercises ? 'page' : undefined}>التمارين</Link>
      </nav>
    </div>
    <div className="staff-library-body">{exercises ? <ExerciseLibrary /> : <LessonsPage preview />}</div>
  </div>
}
