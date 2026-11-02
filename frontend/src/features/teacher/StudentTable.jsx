import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../../auth/useAuth'
import { studentPath } from '../../layout/staffNavigation'
import { CompletionBar } from './StaffUi'
import { formatDate } from './staffFormat'

export default function StudentTable({ students, empty = 'لا يوجد طلاب مطابقون.' }) {
  const { student: account } = useAuth()
  const location = useLocation()
  const backTo = location.pathname.endsWith('/students') ? location.pathname + location.search
    : account.is_admin ? '/admin/students' : '/teacher/students'
  return <div className="staff-table-wrap student-table-wrap"><table className="staff-table student-table" aria-label="قائمة الطلاب ونتائجهم">
    <thead><tr>{['الطالب','رقم الطالب','الشعبة','الإتمام','دقة الإجابات','النقاط','آخر نشاط',''].map((h,i) => <th key={i}>{h}</th>)}</tr></thead>
    <tbody>{students.map(s => <tr key={s.student_id}>
      <td className="student-identity"><Link to={studentPath(account, s.student_id)} state={{ backTo }}>{s.name}</Link>
        <div className="staff-secondary" dir="ltr">{s.email}</div></td>
      <td data-label="رقم الطالب"><bdi>{s.student_number || '—'}</bdi></td>
      <td data-label="الشعبة">{s.class_section || 'لم يحددها بعد'}</td>
      <td data-label="الإتمام"><CompletionBar value={s.completion_pct} /><div className="staff-secondary">{s.lessons_done} درس مكتمل</div></td>
      <td data-label="دقة الإجابات">{s.accuracy_pct == null ? '—' : s.accuracy_pct + '%'}
        <div className="staff-secondary">{s.answers_count} إجابة</div></td>
      <td data-label="النقاط">{s.total_score}</td><td data-label="آخر نشاط">{formatDate(s.last_active)}</td>
      <td className="student-details"><Link to={studentPath(account, s.student_id)} state={{ backTo }}>عرض ملف الطالب ←</Link></td>
    </tr>)}
    {!students.length && <tr><td colSpan={8} className="staff-empty">{empty}</td></tr>}
    </tbody>
  </table></div>
}
