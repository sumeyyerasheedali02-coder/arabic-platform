import { Link } from 'react-router-dom'
import api from '../../api/client'
import { useStaffApiData } from '../staff/useStaffApiData'
import { useAuth } from '../../auth/useAuth'
import { CenteredSpinner } from '../../components/Spinner'
import { useStaff } from '../staff/useStaff'
import { StaffMessage, StaffStats } from '../teacher/StaffUi'
import { apiError } from '../teacher/staffFormat'
import SectionCards from './SectionCards'

export default function AdminPage() {
  const { student } = useAuth()
  const sections = useStaff()
  const report = useStaffApiData(`admin-overview:${student.id}`, () => Promise.all([
    api.get('/admin/teachers'), api.get('/teacher/students'),
  ]).then(([teachers, students]) => ({
    teachers: teachers.data, students: students.data,
  })))
  function refresh() { sections.reload(); report.reload() }
  if (sections.loading || report.loading) return <CenteredSpinner size={32} height={260} />
  if (sections.error || report.error) return <div className="staff-page">
    <StaffMessage error={apiError(sections.error || report.error)} onRetry={refresh} />
  </div>
  const teachers = report.data?.teachers ?? []
  const students = report.data?.students ?? []
  const unassigned = (sections.data ?? []).filter(s => !s.teachers_count)
  const withoutSection = students.filter(s => !s.class_section)
  const average = students.length
    ? Math.round(students.reduce((n,s) => n + s.completion_pct, 0) / students.length) + '%' : '—'
  return <div className="staff-page" dir="rtl">
    <div className="staff-toolbar"><h1>نظرة عامة على المنصة</h1></div>
    <p className="staff-intro">مرحبًا {student.name}. إليك توزيع الحسابات وتقدّم الطلاب وما يحتاج متابعة.</p>
    <StaffStats items={[
      ['عدد الطلاب', students.length], ['المدرسون النشطون', teachers.filter(t => t.is_active).length],
      ['الشُّعَب', sections.data?.length ?? 0], ['متوسط إتمام الدروس', average],
    ]} />
    <div className="staff-admin-actions">
      <Link className="staff-button staff-primary" to="/admin/teachers">إدارة المدرسين</Link>
      <Link className="staff-button" to="/admin/students">متابعة الطلاب</Link>
      <Link className="staff-button" to="/content">معاينة المحتوى</Link>
    </div>
    {(unassigned.length > 0 || withoutSection.length > 0) && <section className="staff-panel staff-attention">
      <h2>يحتاج انتباهك</h2>
      {unassigned.length > 0 && <p>شُعَب دون مدرس نشط: {unassigned.map(s => s.class_section).join('، ')}.
        <Link to="/admin/teachers"> إسناد المدرسين</Link></p>}
      {withoutSection.length > 0 && <p>{withoutSection.length} طالبًا لم يحددوا شُعَبهم بعد.
        <Link to="/admin/students"> مراجعة الطلاب</Link></p>}
    </section>}
    <section className="staff-panel"><div className="staff-toolbar"><h2>توزيع الشُّعَب</h2>
      <Link className="staff-button" to="/admin/sections">تفاصيل الشُّعَب</Link></div>
      <SectionCards sections={sections.data ?? []} teachers={teachers} />
    </section>
  </div>
}
