import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/useAuth'
import { completedLessons, useProgress } from '../features/progress/useProgress'
import { useUnits } from '../features/units/useUnits'
import StaffSidebar from './StaffSidebar'

const AR_NUMS = ['١','٢','٣','٤','٥','٦','٧','٨','٩','١٠']

function KBULogo() {
  return (
    <svg width="32" height="32" viewBox="0 0 32 32">
      <circle cx="16" cy="16" r="15" fill="none" stroke="#C9A84C" strokeWidth="1.5" />
      <circle cx="16" cy="16" r="10" fill="none" stroke="#C9A84C" strokeWidth="1" opacity=".5" />
      <text x="16" y="20" textAnchor="middle" fill="#C9A84C" fontSize="9" fontWeight="700"
        fontFamily="DM Sans, sans-serif" letterSpacing=".05em">KBÜ</text>
    </svg>
  )
}

// Pages that show the selected unit themselves; from anywhere else, choosing a
// unit opens its lessons.
const UNIT_PAGES = ['/lessons', '/exercises']

export default function Sidebar({ open, phone, sidebarRef, onNavigate }) {
  const { student, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const { units, selectedUnit, selectUnit } = useUnits()
  const { progress } = useProgress()

  const openUnit = (unit) => {
    selectUnit(unit)
    if (!UNIT_PAGES.includes(location.pathname)) navigate('/lessons')
    onNavigate?.()
  }

  const totalLessons    = units.reduce((s, u) => s + (u.total_lessons || 0), 0)
  const doneLessons     = completedLessons(progress).length
  const progressPct     = totalLessons > 0 ? Math.round((doneLessons / totalLessons) * 100) : 0
  if (student?.is_teacher || student?.is_admin) return <StaffSidebar open={open} phone={phone} sidebarRef={sidebarRef} onNavigate={onNavigate} />

  return (
    <aside id="app-sidebar" ref={sidebarRef} inert={phone && !open} role={open ? 'dialog' : undefined} aria-modal={open || undefined} aria-label="الوحدات والحساب" tabIndex={-1} className={`app-sidebar${open ? ' open' : ''}`} style={{
      background: 'var(--navy)',
      display: 'flex',
      flexDirection: 'column',
      borderLeft: '1px solid rgba(255,255,255,.06)',
    }}>
      <button className="sidebar-close" onClick={onNavigate} aria-label="إغلاق القائمة">×</button>
      {/* University identity */}
      <div style={{ padding: '20px 18px 16px', borderBottom: '1px solid rgba(201,168,76,.2)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <KBULogo />
          <div>
            <div style={{ fontSize: 11, color: '#fff', fontWeight: 500 }}>Karabük Üniversitesi</div>
            <div style={{ fontSize: 9, color: 'rgba(255,255,255,.4)', letterSpacing: '.06em' }}>
              İLAHİYAT FAKÜLTESİ
            </div>
          </div>
        </div>
      </div>

      {/* Keep the title outside the scrolling unit list. */}
      <div id="sidebar-units-title" style={{
        fontSize: 12, letterSpacing: '.07em', color: 'rgba(255,255,255,.5)',
        padding: '14px 16px 10px', fontWeight: 600,
      }}>
        UNITS — الوحدات
      </div>
      <nav className="sidebar-units" aria-labelledby="sidebar-units-title" style={{ flex: 1, overflowY: 'auto', padding: '0 0 4px' }}>
        {units.map((unit, i) => {
          const isActive = selectedUnit?.id === unit.id
          return (
            <button type="button" className="sidebar-unit" aria-current={isActive ? 'true' : undefined}
              key={unit.id}
              onClick={() => openUnit(unit)}
              style={{
                display: 'flex', alignItems: 'flex-start', gap: 10,
                padding: '9px 16px', cursor: 'pointer',
                borderRight: isActive ? '3px solid #C9A84C' : '3px solid transparent',
                background: isActive ? 'rgba(201,168,76,.1)' : 'transparent',
                transition: 'all .18s',
              }}
              onMouseEnter={e => { if (!isActive) e.currentTarget.style.background = 'rgba(201,168,76,.05)' }}
              onMouseLeave={e => { if (!isActive) e.currentTarget.style.background = 'transparent' }}
            >
              <div style={{
                width: 22, height: 22, borderRadius: 6, flexShrink: 0,
                background: isActive ? '#C9A84C' : 'rgba(255,255,255,.08)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 10, fontWeight: 500,
                color: isActive ? 'var(--navy)' : 'rgba(255,255,255,.6)',
              }}>
                {AR_NUMS[i] || i + 1}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{
                  fontSize: 13, fontFamily: "'Amiri', serif",
                  color: isActive ? '#fff' : 'rgba(255,255,255,.8)',
                  whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
                }}>
                  {unit.title_ar}
                </div>
                <div style={{ fontSize: 10, color: 'rgba(255,255,255,.35)', marginTop: 1 }}>
                  {unit.title_tr}
                </div>
              </div>
            </button>
          )
        })}
      </nav>

      {/* Overall progress */}
      <div style={{ padding: 16, borderTop: '1px solid rgba(255,255,255,.06)' }}>
        {student && <Link to="/account" onClick={onNavigate} style={{ display: 'block', marginBottom: 12,
          color: '#E8D48A', fontSize: 12, textDecoration: 'none' }}>إعدادات الحساب</Link>}
        {student && !student.is_teacher && !student.is_admin && <div style={{ background: 'rgba(255,255,255,.06)', borderRadius: 9, padding: '10px 12px', marginBottom: 10 }}>
          <div style={{ fontSize: 9, color: 'rgba(255,255,255,.4)', marginBottom: 6, letterSpacing: '.08em' }}>
            OVERALL PROGRESS
          </div>
          <div style={{ height: 4, background: 'rgba(255,255,255,.12)', borderRadius: 2, overflow: 'hidden' }}>
            <div style={{ height: '100%', background: '#C9A84C', borderRadius: 2, width: `${progressPct}%`, transition: 'width .4s' }} />
          </div>
          <div style={{ fontSize: 11, color: '#C9A84C', marginTop: 5, fontWeight: 500 }}>
            {progressPct}% مكتمل
          </div>
        </div>}

        {/* Student info + logout / guest */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <div style={{
            width: 28, height: 28, borderRadius: '50%',
            background: student ? '#C9A84C' : 'rgba(255,255,255,.15)',
            color: student ? 'var(--navy)' : 'rgba(255,255,255,.6)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 10, fontWeight: 700, flexShrink: 0,
            border: student ? 'none' : '1px solid rgba(255,255,255,.2)',
          }}>
            {student ? student.name.split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase() : '؟'}
          </div>
          <div style={{ flex: 1, minWidth: 0 }}>
            {student ? (
              <div style={{ fontSize: 11, color: '#fff', fontWeight: 500, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {student.name}
              </div>
            ) : (
              <>
                <div style={{ fontSize: 11, color: 'rgba(255,255,255,.55)', fontWeight: 500 }}>ضيف</div>
                <div style={{ fontSize: 9, color: 'rgba(255,255,255,.25)', marginTop: 1 }}>Guest Mode</div>
              </>
            )}
          </div>
          <button
            onClick={() => { logout(); navigate('/login') }}
            style={{
              background: 'none', border: '1px solid rgba(255,255,255,.15)',
              borderRadius: 6, cursor: 'pointer', padding: '3px 7px',
              color: 'rgba(255,255,255,.45)', fontSize: 10,
              fontFamily: 'DM Sans, sans-serif', transition: 'all .15s',
            }}
            title={student ? 'تسجيل الخروج' : 'تسجيل الدخول'}
            onMouseEnter={e => { e.currentTarget.style.background = 'rgba(255,255,255,.08)'; e.currentTarget.style.color = '#fff' }}
            onMouseLeave={e => { e.currentTarget.style.background = 'none'; e.currentTarget.style.color = 'rgba(255,255,255,.45)' }}
          >
            {student ? 'خروج' : 'دخول'}
          </button>
        </div>
      </div>
    </aside>
  )
}
