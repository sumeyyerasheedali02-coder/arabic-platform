import { Link } from 'react-router-dom'

export default function SectionCards({ sections, teachers }) {
  return <div className="staff-unit-grid">{sections.map(s => {
    const assigned = teachers.filter(t => t.is_active && t.sections.includes(s.class_section))
    return <article className="staff-section-card" key={s.class_section}>
      <strong>الشعبة {s.class_section}</strong>
      <span>{s.students_count} طالبًا · {s.teachers_count} مدرسًا نشطًا</span>
      <p>{assigned.length ? assigned.map(t => t.name).join('، ') : 'لم يُسند مدرس نشط لهذه الشعبة.'}</p>
      <div className="staff-actions">
        <Link className="staff-button" to={`/admin/students?section=${s.class_section}`}>عرض الطلاب</Link>
        <Link className="staff-button" to="/admin/teachers">إدارة المدرسين</Link>
      </div>
    </article>
  })}</div>
}
