import { Link } from 'react-router-dom'
import { useAuth } from '../../auth/useAuth'
import { studentPath } from '../../layout/staffNavigation'
import { formatDateTime } from './staffFormat'

export default function RecentActivity({ items }) {
  const { student } = useAuth()
  return <section className="staff-panel">
    <h2>آخر نتائج التمارين</h2>
    <div className="staff-table-wrap"><table className="staff-table">
      <thead><tr><th>الطالب</th><th>السؤال</th><th>النتيجة</th><th>الوقت</th></tr></thead>
      <tbody>{items.map(item => <tr key={item.id}>
        <td><Link to={studentPath(student, item.student_id)}>{item.name}</Link>
          <div className="staff-secondary">الشعبة {item.class_section || '—'}</div></td>
        <td>{item.question_ar}</td>
        <td><span className={`staff-badge ${item.is_correct ? '' : 'staff-badge-review'}`}>
          {item.is_correct ? 'صحيحة' : 'تحتاج مراجعة'}</span></td>
        <td>{formatDateTime(item.answered_at)}</td>
      </tr>)}
      {!items.length && <tr><td colSpan={4} className="staff-empty">لا توجد نتائج تمارين مسجلة بعد.</td></tr>}
      </tbody>
    </table></div>
  </section>
}
