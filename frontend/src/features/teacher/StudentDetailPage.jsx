import { useEffect, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import api from '../../api/client'
import { useStaffApiData } from '../staff/useStaffApiData'
import { useAuth } from '../../auth/useAuth'
import { CenteredSpinner } from '../../components/Spinner'
import { CompletionBar, StaffMessage, StaffStats } from './StaffUi'
import { apiError, formatDate } from './staffFormat'
import { useStaff } from '../staff/useStaff'
import { formatStudyTime } from '../activity/activeClock'

const STATUS = { completed: 'مكتمل', in_progress: 'قيد التعلّم', not_started: 'لم يبدأ' }

function SectionCorrection({ student, onSaved }) {
  const [section, setSection] = useState(student.class_section || '')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [saved, setSaved] = useState(false)
  async function save(event) {
    event.preventDefault()
    setSaving(true); setError(''); setSaved(false)
    try {
      await api.patch(`/admin/students/${student.student_id}/section`, { class_section: section })
      setSaved(true); onSaved()
    } catch (err) { setError(apiError(err)) }
    finally { setSaving(false) }
  }
  return <section className="staff-panel">
    <h2>تصحيح شعبة الطالب</h2>
    <form onSubmit={save} className="staff-toolbar">
      <label htmlFor="correct-section">الشعبة</label>
      <select id="correct-section" required value={section} disabled={saving}
        onChange={e => { setSection(e.target.value); setSaved(false) }}>
        <option value="" disabled>اختر الشعبة</option>
        {['A','B','C','D'].map(s => <option key={s} value={s}>الشعبة {s}</option>)}
      </select>
      <button className="staff-primary" disabled={saving || !section || section === student.class_section}>
        {saving ? 'جارٍ الحفظ…' : 'حفظ الشعبة'}
      </button>
    </form>
    {saved && <div role="status" className="staff-success">حُفظت الشعبة مع الحفاظ على تقدّم الطالب.</div>}
    {error && <StaffMessage error={error} />}
  </section>
}

export default function StudentDetailPage() {
  const { studentId } = useParams()
  const { student: account } = useAuth()
  const sections = useStaff()
  const location = useLocation()
  const report = useStaffApiData(`student-detail:${account.id}:${studentId}`,
    () => api.get(`/teacher/students/${studentId}`).then(r => r.data))
  const [onlyStarted, setOnlyStarted] = useState(false)
  const refreshReport = report.reload
  useEffect(() => {
    const timer = setInterval(() => {
      if (document.visibilityState === 'visible') refreshReport()
    }, 30_000)
    return () => clearInterval(timer)
  }, [refreshReport])
  const studentsPath = location.state?.backTo || (account.is_admin ? '/admin/students' : '/teacher/students')
  if (report.loading) return <CenteredSpinner size={32} height={260} />
  if (report.error) return <div className="staff-page">
    <Link className="staff-button" to={studentsPath}>العودة لقائمة الطلاب</Link>
    <StaffMessage error={apiError(report.error)} onRetry={report.reload} />
  </div>
  if (!report.data) return null
  const { student, lessons, history, recent_errors: errors } = report.data
  const visible = onlyStarted ? lessons.filter(l => l.status !== 'not_started') : lessons
  return <div className="staff-page" dir="rtl">
    <div className="staff-toolbar">
      <Link className="staff-button" to={studentsPath}>العودة لقائمة الطلاب</Link>
      {account.is_admin && <Link className="staff-button" to="/admin">إدارة المنصة</Link>}

    </div>
    <h1>{student.name}</h1>
    <p className="staff-intro">{student.email} · رقم الطالب: {student.student_number || 'لم يُدخل بعد'} · {student.class_section
      ? `الشعبة ${student.class_section}` : 'لم يحدد شعبته بعد'} · آخر نشاط: {formatDate(student.last_active)}</p>
    <StaffStats items={[
      ['إتمام الدروس', student.completion_pct + '%'],
      ['دقة الإجابات', student.accuracy_pct == null ? '—' : student.accuracy_pct + '%'],
      ['أفضل نقاط التمارين', student.total_score],
      ['عدد الإجابات', student.answers_count],
      ['وقت الاستخدام الفعلي', formatStudyTime(student.active_time_sec)],
    ]} />
    {account.is_admin && <SectionCorrection key={student.student_id} student={student}
      onSaved={() => { report.reload(); sections.reload() }} />}
    <section className="staff-panel">
      <div className="staff-toolbar"><h2>التقدّم في الدروس</h2>
        <label><input type="checkbox" checked={onlyStarted}
          onChange={e => setOnlyStarted(e.target.checked)} /> الدروس التي بدأها فقط</label>
      </div>
      <div className="staff-table-wrap"><table className="staff-table">
        <thead><tr>{['الوحدة والدرس','الحالة','أفضل نقاط الجلسة','جلسات التدريب','الوقت المسجل','آخر تحديث'].map(h => <th key={h}>{h}</th>)}</tr></thead>
        <tbody>{visible.map(l => <tr key={l.id}>
          <td>{l.title_ar}<div className="staff-secondary">{l.unit_number}. {l.unit_title}</div></td>
          <td><span className={`staff-badge ${l.status === 'not_started' ? 'inactive' : ''}`}>{STATUS[l.status]}</span></td>
          <td>{l.score ?? 0}</td><td>{l.attempts ?? 0}</td>
          <td>{formatStudyTime(l.time_spent_sec)}</td><td>{formatDate(l.updated_at)}</td>
        </tr>)}
        {!visible.length && <tr><td colSpan={6} className="staff-empty">لم يبدأ الطالب أي درس بعد.</td></tr>}
        </tbody>
      </table></div>
      <p className="staff-intro" style={{ margin: '14px 0 0' }}>
        الإتمام يعكس جلسات التدريب المسجلة. دقة الإجابات مؤشر مستقل لنتائج التمارين.
        {' '}الوقت يُحفظ كل 15 ثانية أثناء ظهور الصفحة؛ يتوقف عند مغادرتها أو بعد 90 ثانية دون تفاعل. القياس الجديد يبدأ من تاريخ تفعيله.
      </p>
    </section>
    <section className="staff-panel">
      <h2>نتائج التدريب خلال آخر 30 يومًا</h2>
      {history.length ? <div className="staff-table-wrap"><table className="staff-table">
        <thead><tr><th>اليوم</th><th>الإجابات</th><th>الصحيحة</th><th>الدقة</th></tr></thead>
        <tbody>{history.map(d => <tr key={d.date}>
          <td>{d.date}</td><td>{d.answers}</td><td>{d.correct}</td>
          <td><CompletionBar value={Math.round(d.correct / d.answers * 100)} /></td>
        </tr>)}</tbody>
      </table></div> : <p className="staff-empty">لا توجد إجابات مسجلة خلال هذه الفترة.</p>}
    </section>
    <section className="staff-panel">
      <h2>آخر الإجابات الخاطئة · حتى 10 إجابات</h2>
      {errors.length ? errors.map((e,i) => <div className="staff-error-item" key={i}>
        <strong>{e.question_ar}</strong><p>إجابة الطالب: {e.student_answer}</p>
        <p>الإجابة الصحيحة: {e.correct_answer}</p>
        <span className="staff-intro">{formatDate(e.answered_at)}</span>
      </div>) : <p className="staff-empty">لا توجد إجابات خاطئة مسجلة.</p>}
    </section>
  </div>
}
