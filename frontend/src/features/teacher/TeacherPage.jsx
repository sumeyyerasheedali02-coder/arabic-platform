import { useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import api from '../../api/client'
import { useStaffApiData } from '../staff/useStaffApiData'
import { useAuth } from '../../auth/useAuth'
import { CenteredSpinner } from '../../components/Spinner'
import { useStaff } from '../staff/useStaff'
import { CompletionBar, StaffMessage, StaffStats } from './StaffUi'
import { apiError } from './staffFormat'
import StudentTable from './StudentTable'
import RecentActivity from './RecentActivity'
import { normalizeStudentNumber } from '../auth/studentNumber'

const needsHelp = s => s.answers_count >= 5 && s.accuracy_pct < 60

export default function TeacherPage({ view = 'overview' }) {
  const { student } = useAuth()
  const [params, setParams] = useSearchParams()
  const [search, setSearch] = useState('')
  const sections = useStaff()
  const selected = params.get('section') || (sections.data?.length === 1 ? sections.data[0].class_section : '')
  const filter = params.get('filter') || 'all'
  const report = useStaffApiData(sections.data ? `staff-report:${student.id}:${selected}:${view}` : null, () => {
    const query = selected ? { section: selected } : {}
    return Promise.all([
      api.get('/teacher/students', { params: query }),
      view === 'overview' ? api.get('/teacher/units/stats', { params: query }) : Promise.resolve({ data: [] }),
    ]).then(([students, units]) => ({ students: students.data, units: units.data }))
  })
  const activity = useStaffApiData(view === 'overview' && sections.data
    ? `staff-activity:${student.id}:${selected}` : null,
    () => api.get('/teacher/activity', { params: selected ? { section: selected } : {} }).then(r => r.data))
  function changeParam(key, value) {
    const next = new URLSearchParams(params)
    if (value && value !== 'all') next.set(key, value)
    else next.delete(key)
    setParams(next)
  }
  function refresh() { sections.reload(); report.reload(); activity.reload() }
  if (sections.loading || report.loading || activity.loading) return <CenteredSpinner size={32} height={280} />
  const error = sections.error || report.error || activity.error
  if (error) return <div className="staff-page"><StaffMessage error={apiError(error)} onRetry={refresh} /></div>
  const students = report.data?.students ?? []
  const units = report.data?.units ?? []
  const answers = students.reduce((n, s) => n + s.answers_count, 0)
  const correct = students.reduce((n, s) => n + s.correct_answers, 0)
  const visible = students.filter(s =>
    `${s.name} ${s.email} ${s.student_number || ''}`.toLowerCase().includes(normalizeStudentNumber(search).toLowerCase())
    && (filter === 'all' || (filter === 'help' ? needsHelp(s) : s.answers_count === 0)))
  const base = student.is_admin ? '/admin/students' : '/teacher/students'
  const filteredLink = `${base}?${new URLSearchParams({ ...(selected ? { section: selected } : {}), filter: 'help' })}`
  return <div className="staff-page" dir="rtl">
    <h1>{view === 'overview' ? 'نظرة عامة على شُعَبي' : student.is_admin ? 'الطلاب والمتابعة' : 'طلابي'}</h1>
    <p className="staff-intro">{view === 'overview'
      ? `مرحبًا ${student.name}. إليك تقدّم طلابك والنتائج التي تحتاج انتباهك.`
      : 'ابحث عن الطالب وافتح ملفه لمتابعة الدروس والنتائج والأخطاء.'}</p>
    {!student.is_admin && sections.data?.length === 0
      ? <div className="staff-panel staff-empty">لم تُسند إليك شعبة بعد. تواصل مع مدير المنصة.</div>
      : <>
        <div className="staff-toolbar">
          <label htmlFor="report-section">الشعبة</label>
          <select id="report-section" value={selected} onChange={e => changeParam('section', e.target.value)}>
            {sections.data?.length !== 1 && <option value="">جميع الشُّعَب {student.is_admin ? '' : 'المسندة إليك'}</option>}
            {sections.data?.map(s => <option value={s.class_section} key={s.class_section}>
              الشعبة {s.class_section} · {s.students_count} طالبًا
            </option>)}
          </select>

        </div>
        <StaffStats items={[
          ['عدد الطلاب', students.length],
          ['متوسط الإتمام', students.length
            ? Math.round(students.reduce((n, s) => n + s.completion_pct, 0) / students.length) + '%' : '—'],
          ['دقة الإجابات', answers ? Math.round(correct / answers * 100) + '%' : '—'],
          ['يحتاجون متابعة', students.filter(needsHelp).length],
        ]} />
        {view === 'overview' ? <>
          <section className="staff-panel">
            <h2>شُعَبي</h2>
            <div className="staff-unit-grid">{(sections.data ?? []).map(s =>
              <Link className="staff-section-card" to={`${base}?section=${s.class_section}`} key={s.class_section}>
                <strong>الشعبة {s.class_section}</strong><span>{s.students_count} طالبًا</span>
                <small>عرض الطلاب ←</small>
              </Link>)}</div>
          </section>
          <section className="staff-panel">
            <div className="staff-toolbar"><h2>طلاب يحتاجون متابعة</h2>
              <Link className="staff-button" to={filteredLink}>عرض القائمة</Link>
            </div>
            <StudentTable students={students.filter(needsHelp).slice(0, 5)} empty="لا يوجد طلاب تنطبق عليهم مؤشرات المتابعة حاليًا." />
            <p className="staff-intro" style={{ margin: '14px 0 0' }}>المؤشر: دقة أقل من 60% بعد خمس إجابات على الأقل.</p>
          </section>
          <RecentActivity items={activity.data ?? []} />
          <details className="staff-panel staff-unit-details">
            <summary>تقدّم الشُّعَب في الوحدات</summary>
            <div className="staff-unit-grid">{units.map(u => <div className="staff-unit" key={u.unit_number}>
              <h3>{u.unit_number}. {u.title_ar}</h3><CompletionBar value={u.completion_pct} />
              <p>متوسط نقاط الدروس التي بدأها الطلاب: {u.avg_score}</p>
            </div>)}</div>
          </details>
        </> : <section className="staff-panel">
          <div className="staff-toolbar"><h2>قائمة الطلاب</h2>
            <input className="staff-search" aria-label="البحث عن طالب" placeholder="ابحث بالاسم أو البريد أو رقم الطالب"
              value={search} onChange={e => setSearch(e.target.value)} />
            <select aria-label="تصفية الطلاب" value={filter} onChange={e => changeParam('filter', e.target.value)}>
              <option value="all">جميع الطلاب</option><option value="help">يحتاجون متابعة</option>
              <option value="new">لم يجيبوا عن تمارين بعد</option>
            </select>
          </div>
          <StudentTable students={visible} />
          <p className="staff-intro" style={{ margin: '14px 0 0' }}>
            يحتاج متابعة: دقة أقل من 60% بعد خمس إجابات على الأقل. هذا مؤشر للمراجعة مع الأستاذ.
          </p>
        </section>}
      </>}
  </div>
}
