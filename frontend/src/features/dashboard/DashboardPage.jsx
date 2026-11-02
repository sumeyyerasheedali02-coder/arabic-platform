import { useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import { useAuth } from '../../auth/useAuth'
import ErrorState from '../../components/ErrorState'
import { CenteredSpinner } from '../../components/Spinner'
import { completedLessons, useProgress } from '../progress/useProgress'
import { useUnits } from '../units/useUnits'
import { formatStudyTime } from '../activity/activeClock'
import './journey.css'

export default function DashboardPage() {
  const { student, token } = useAuth()
  const { units, selectUnit, loading: loadingUnits, error: unitsError, reload: reloadUnits } = useUnits()
  const { progress, loading, error, reload } = useProgress()
  const [filter, setFilter] = useState('in_progress')
  const due = useApiData(token ? 'srs-due-count' : null, () => api.get('/me/srs/due').then(r => r.data.length))
  const total = units.reduce((sum, unit) => sum + (unit.total_lessons || 0), 0)
  const done = completedLessons(progress).length
  const percent = total ? Math.min(100, Math.round(done / total * 100)) : 0
  const rows = units.map(unit => {
    const entries = progress.filter(p => p.unit_id === unit.id)
    const completed = entries.filter(p => p.status === 'completed').length
    const status = unit.total_lessons > 0 && completed >= unit.total_lessons ? 'completed'
      : entries.some(p => p.status !== 'not_started') ? 'in_progress' : 'not_started'
    return { unit, completed, status, percent: unit.total_lessons ? Math.min(100, Math.round(completed / unit.total_lessons * 100)) : 0 }
  })
  const next = rows.find(row => row.status === 'in_progress') ?? rows.find(row => row.status === 'not_started')
  const visible = rows.filter(row => row.status === filter)
  const seconds = progress.reduce((sum, p) => sum + (p.time_spent_sec || 0), 0)
  if (loadingUnits || loading) return <CenteredSpinner size={32} height={260} />
  if (unitsError || error) return <ErrorState onRetry={() => { reloadUnits(); reload() }} />
  return <div className="journey-page" dir="rtl">
    <header className="journey-heading"><div><span className="journey-eyebrow">خطوة بعد خطوة</span><h1>رحلتي مع العربية</h1></div><span className="journey-name">{student?.name || 'مرحبًا بك'}</span></header>
    {!token ? <section className="journey-hero"><h2>ابدأ رحلتك، واحفظ كل خطوة</h2><p>سجّل الدخول لعرض تقدّمك ومتابعة دروسك.</p><Link className="journey-primary" to="/login">تسجيل الدخول ←</Link></section> : <>
      <section className="journey-hero">
        <div className="journey-hero-copy"><span className="journey-eyebrow">تقدّمك في المنهج</span><h2>{done ? 'كل درس يقرّبك أكثر' : 'رحلتك تبدأ من هنا'}</h2><p>{done} من {total} درس مكتمل</p>
          {next ? <Link className="journey-primary" to="/lessons" onClick={() => selectUnit(next.unit)}>أكمل تعلّمك <span aria-hidden="true">←</span></Link> : <Link className="journey-primary" to="/lessons">راجع دروسك ←</Link>}
          {next && <span className="journey-next">الوحدة {next.unit.unit_number} · {next.unit.title_ar}</span>}
        </div>
        <div className="journey-ring" style={{ '--completion': `${percent}%` }} role="progressbar" aria-label="إتمام المنهج" aria-valuenow={percent} aria-valuemin={0} aria-valuemax={100}><div><strong>{percent}<small>%</small></strong><span>من المنهج</span></div></div>
      </section>
      <div className="journey-metrics">
        <section><span className="journey-metric-mark" aria-hidden="true">✓</span><div><span>الدروس المكتملة</span><strong>{done}<small> / {total}</small></strong></div></section>
        <section><span className="journey-metric-mark" aria-hidden="true">◷</span><div><span>وقت دراسة الدروس</span><strong className="journey-time">{formatStudyTime(seconds)}</strong></div></section>
        <section><span className="journey-metric-mark" aria-hidden="true">▤</span><div><span>بطاقات للمراجعة</span>{due.error ? <button onClick={due.reload}>أعد المحاولة</button> : <Link to="/srs" className="journey-review">{due.loading ? '…' : due.data ?? 0}<small> راجع الآن ←</small></Link>}</div></section>
      </div>
    </>}
    <section className="journey-units"><div className="journey-section-title"><h2>وحداتي الدراسية</h2><span>{units.length} وحدة</span></div>
      <div className="journey-filters" role="group" aria-label="حالة الوحدات">{[['in_progress','قيد التعلّم'],['completed','مكتملة'],['not_started','لم تبدأ']].map(([value,label]) => <button key={value} aria-pressed={filter === value} onClick={() => setFilter(value)}>{label}<span>{rows.filter(row => row.status === value).length}</span></button>)}</div>
      {visible.length ? <div className="journey-unit-list">{visible.map(({ unit, completed, percent: pct, status }) => <Link key={unit.id} className="journey-unit" to="/lessons" onClick={() => selectUnit(unit)}>
        <img src={`${import.meta.env.BASE_URL}images/units/unit-${String(unit.unit_number).padStart(2,'0')}-scene-small.webp?v=2`} alt="" width="84" height="70" loading="lazy" />
        <div className="journey-unit-copy"><span>الوحدة {unit.unit_number}</span><h3>{unit.title_ar}</h3><p lang="tr" dir="ltr">{unit.title_tr}</p><div className="journey-unit-progress"><span style={{ width: `${pct}%` }} /></div><span>{completed} من {unit.total_lessons} دروس · {pct}%</span></div>
        <span className="journey-unit-arrow" aria-hidden="true">{status === 'completed' ? '✓' : '←'}</span>
      </Link>)}</div> : <div className="journey-empty"><span aria-hidden="true">{filter === 'completed' ? '✓' : '—'}</span><h3>{filter === 'completed' ? 'ستجد هنا الوحدات التي تكملها' : filter === 'in_progress' ? 'لا توجد وحدات قيد التعلّم' : 'بدأت جميع الوحدات'}</h3><p>{filter === 'in_progress' ? 'اختر وحدة من «لم تبدأ» لبدء التعلّم.' : 'تابع رحلتك من صفحة الدروس.'}</p></div>}
    </section>
  </div>
}
