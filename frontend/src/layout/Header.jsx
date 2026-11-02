import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/useAuth'
import { staffHome, staffPageTitle } from './staffNavigation'
import TrackingLink from '../components/TrackingLink'

const NAV = [
  { to: '/lessons',   label: 'الدروس', icon: 'book' },
  { to: '/exercises', label: 'التدريبات', icon: 'practice' },
  { to: '/shared-words', label: 'مفردات مشتركة', shortLabel: 'مفردات', icon: 'words' },
  { to: '/srs',       label: 'بطاقات الحفظ', shortLabel: 'البطاقات', icon: 'cards' },
  { to: '/dashboard', label: 'تقدمي', icon: 'progress' },
]

function NavigationIcon({ name }) {
  const paths = {
    book: <><path d="M12 5c-3-2-6-2-9-1v15c3-1 6-1 9 1m0-15c3-2 6-2 9-1v15c-3-1-6-1-9 1V5" /></>,
    words: <><path d="M3 5h12M8 3v2M5 5c1 5 4 8 8 10M13 5c-1 5-5 8-10 11M14 21l4-10 4 10M15 18h6" /></>,
    cards: <><rect x="6" y="6" width="15" height="15" rx="3" /><path d="M3 16V6a3 3 0 0 1 3-3h10m-5 9h5m-5 4h3" /></>,
    practice: <><rect x="4" y="3" width="16" height="18" rx="3" /><path d="m8 9 2 2 5-5M8 16h8" /></>,
    progress: <><path d="M4 3v18h17M8 15l4-5 4 2 5-7" /></>,
  }
  return <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name]}</svg>
}

export default function Header({ onMenuClick, menuOpen }) {
  const { student, logout } = useAuth()
  const location  = useLocation()
  const navigate  = useNavigate()
  const isStaff = student?.is_teacher || student?.is_admin

  const handleLogout = () => { logout(); navigate('/login') }

  return (
    <header className="app-header">
      {/* Menu button — mobile only (opens the sidebar drawer) */}
      <button className="hdr-menu-btn" onClick={onMenuClick} aria-label="فتح القائمة" aria-expanded={menuOpen} aria-controls="app-sidebar">☰</button>

      {/* Platform logo */}
      <div className="hdr-logo" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: 140, flexShrink: 0 }}>
        <div style={{ fontFamily: "'Amiri', serif", fontSize: 17, color: 'var(--navy)', lineHeight: 1.2 }}>
          مَنْصَّةُ تَعَلُّمِ الْعَرَبِيَّة
        </div>
        <div className="hdr-logo-sub" style={{ fontSize: 8.5, color: 'var(--muted)', letterSpacing: '.1em', marginTop: 2 }}>
          ARABIC LEARNING PLATFORM
        </div>
      </div>

      {/* Divider */}
      <div className="hdr-divider" style={{ width: 1, height: 34, background: 'var(--border)', flexShrink: 0 }} />

      {/* Nav links */}
      {isStaff ? <div className="staff-header-context">
        <strong>{staffPageTitle(location.pathname, student.is_admin)}</strong>
        {location.pathname !== staffHome(student) && <Link to={staffHome(student)}>الرئيسية</Link>}
      </div> : <nav className="hdr-nav" aria-label="التنقل الرئيسي">
        {NAV.map(({ to, label, shortLabel, icon }) => {
          const active = location.pathname === to || (to === '/lessons' && location.pathname.startsWith('/lessons/'))
          return <Link key={to} to={to} aria-label={label} className={`hdr-nav-link${active ? ' is-active' : ''}`} aria-current={active ? 'page' : undefined}>
            <NavigationIcon name={icon} /><span className={shortLabel ? 'hdr-label-full' : undefined}>{label}</span>
            {shortLabel && <span className="hdr-label-short" aria-hidden="true">{shortLabel}</span>}
          </Link>
        })}
      </nav>}

      {student && <TrackingLink />}

      {/* User info + logout */}
      <div className="hdr-account" style={{ display: 'flex', alignItems: 'center', gap: 10, flexShrink: 0 }}>
        {student ? (
          <>
            <div className="hdr-user-text" style={{ textAlign: 'right' }}>
              <div style={{ fontSize: 11.5, fontWeight: 500, color: 'var(--text)' }}>{student.name}</div>
              <div style={{ fontSize: 9.5, color: 'var(--muted)' }}>{student.is_admin ? 'مدير المنصة'
                : student.is_teacher ? 'أستاذ' : 'İlahiyat Fakültesi'}</div>
            </div>
            <Link to="/account" aria-label="إعدادات الحساب" title="إعدادات الحساب" style={{
              width: 34, height: 34, borderRadius: '50%',
              textDecoration: 'none',
              background: 'var(--gold)', color: 'var(--navy)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 11, fontWeight: 600, flexShrink: 0,
            }}>
              {student.name.split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase()}
            </Link>
          </>
        ) : (
          <>
            <div className="hdr-user-text" style={{ textAlign: 'right' }}>
              <div style={{ fontSize: 11.5, fontWeight: 500, color: 'var(--muted)' }}>ضيف</div>
              <div style={{ fontSize: 9.5, color: '#bbb' }}>Guest Mode</div>
            </div>
            <div style={{
              width: 34, height: 34, borderRadius: '50%',
              background: '#e8e4dc', color: '#888',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 13, flexShrink: 0, border: '1px solid var(--border)',
            }}>
              ؟
            </div>
          </>
        )}

        {/* Logout / Login button */}
        <button
          onClick={handleLogout}
          style={{
            marginRight: 4,
            padding: '5px 12px', borderRadius: 7, fontSize: 11.5, fontWeight: 500,
            border: '1px solid var(--border)', background: 'transparent',
            color: 'var(--muted)', cursor: 'pointer', transition: 'all .15s',
            fontFamily: 'DM Sans, sans-serif',
          }}
          onMouseEnter={e => { e.currentTarget.style.background = 'var(--navy)'; e.currentTarget.style.color = '#fff'; e.currentTarget.style.borderColor = 'var(--navy)' }}
          onMouseLeave={e => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = 'var(--muted)'; e.currentTarget.style.borderColor = 'var(--border)' }}
        >
          {student ? 'خروج' : 'دخول'}
        </button>
      </div>
    </header>
  )
}
