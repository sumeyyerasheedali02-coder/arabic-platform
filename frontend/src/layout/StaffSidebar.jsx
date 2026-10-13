import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/useAuth'
import { useStaff } from '../features/staff/useStaff'
import { useUnits } from '../features/units/useUnits'
import { staffLinks } from './staffNavigation'
import '../features/teacher/staff.css'

export default function StaffSidebar({ open, onNavigate }) {
  const { student, logout } = useAuth()
  const { pathname, search } = useLocation()
  const navigate = useNavigate()
  const sections = useStaff()
  const { units, selectedUnit, selectUnit, loading, error, reload } = useUnits()
  const content = pathname.startsWith('/content')
  const selectedSection = new URLSearchParams(search).get('section')
  const studentsPath = student.is_admin ? '/admin/students' : '/teacher/students'
  return <aside className={`app-sidebar staff-sidebar${open ? ' open' : ''}`}>
    <div className="staff-sidebar-brand">
      <div>مَنْصَّةُ تَعَلُّمِ الْعَرَبِيَّة</div>
      <span>Karabük Üniversitesi · İlahiyat</span>
      <strong>{student.is_admin ? 'إدارة المنصة' : 'مساحة الأستاذ'}</strong>
    </div>
    <nav className="staff-sidebar-menu" aria-label={student.is_admin ? 'أقسام الإدارة' : 'أقسام الأستاذ'}>
      {staffLinks(student.is_admin).map(link => {
        const active = link.exact ? pathname === link.to : pathname.startsWith(link.to)
        return <Link key={link.to} to={link.to} onClick={onNavigate}
          aria-current={active ? 'page' : undefined}>{link.label}</Link>
      })}
    </nav>
    <nav className="sidebar-units staff-sidebar-context" aria-label={content ? 'الوحدات التعليمية' : 'الشُّعَب'}>
      <h2>{content ? 'الوحدات التعليمية' : student.is_admin ? 'شُعَب المنصة' : 'شُعَبي'}</h2>
      {(content ? loading : sections.loading) && <p>جارٍ التحميل…</p>}
      {(content ? error : sections.error) && <button onClick={content ? reload : sections.reload}>إعادة تحميل القائمة</button>}
      {content ? units.map(unit => <button key={unit.id} aria-current={selectedUnit?.id === unit.id ? 'true' : undefined}
        onClick={() => { selectUnit(unit); if (pathname !== '/content') navigate('/content'); onNavigate?.() }}>
        <span>{unit.unit_number}. {unit.title_ar}</span><small>{unit.title_tr}</small>
      </button>) : (sections.data ?? []).map(section => <Link key={section.class_section}
        to={`${studentsPath}?section=${section.class_section}`} onClick={onNavigate}
        aria-current={pathname === studentsPath && selectedSection === section.class_section ? 'true' : undefined}>
        <span>الشعبة {section.class_section}</span><small>{section.students_count} طالبًا</small>
      </Link>)}
      {!content && !sections.loading && !sections.error && !sections.data?.length && <p>لم تُسند شُعَب بعد.</p>}
    </nav>
    <div className="staff-sidebar-account">
      <div><strong>{student.name}</strong><small>{student.is_admin ? 'مدير المنصة' : 'أستاذ'}</small></div>
      <button onClick={() => { logout(); navigate('/login') }}>خروج</button>
    </div>
  </aside>
}
