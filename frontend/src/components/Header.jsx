import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const NAV = [
  { to: '/lessons',   label: 'الدروس' },
  { to: '/exercises', label: 'التدريبات' },
  { to: '/srs',       label: 'بطاقات الحفظ' },
  { to: '/chat',      label: 'محادثة AI' },
  { to: '/teacher',   label: 'تقدمي' },
]

export default function Header() {
  const { student, logout } = useAuth()
  const location  = useLocation()
  const navigate  = useNavigate()

  const handleLogout = () => { logout(); navigate('/login') }

  return (
    <header className="app-header" style={{
      background: '#fff',
      borderBottom: '1px solid var(--border)',
      padding: '0 20px',
      display: 'flex', alignItems: 'center', gap: 14,
      position: 'sticky', top: 0, zIndex: 50,
    }}>
      {/* Platform logo */}
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: 170, flexShrink: 0 }}>
        <div style={{ fontFamily: "'Amiri', serif", fontSize: 15, color: 'var(--navy)', lineHeight: 1.2 }}>
          مَنْصَّةُ تَعَلُّمِ الْعَرَبِيَّة
        </div>
        <div style={{ fontSize: 8.5, color: 'var(--muted)', letterSpacing: '.1em', marginTop: 2 }}>
          ARABIC LEARNING PLATFORM
        </div>
      </div>

      {/* Divider */}
      <div style={{ width: 1, height: 28, background: 'var(--border)', flexShrink: 0 }} />

      {/* Nav links */}
      <nav style={{ display: 'flex', gap: 2, flex: 1 }}>
        {NAV.map(({ to, label }) => {
          const active = location.pathname === to || (to === '/lessons' && location.pathname.startsWith('/lessons'))
          return (
            <Link
              key={to}
              to={to}
              style={{
                padding: '6px 11px', borderRadius: 7, fontSize: 11.5, fontWeight: 500,
                textDecoration: 'none', transition: 'all .15s',
                background: active ? 'var(--navy)' : 'transparent',
                color: active ? '#fff' : 'var(--muted)',
              }}
            >
              {label}
            </Link>
          )
        })}
      </nav>

      {/* User info + logout */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexShrink: 0 }}>
        {student ? (
          <>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: 11.5, fontWeight: 500, color: 'var(--text)' }}>{student.name}</div>
              <div style={{ fontSize: 9.5, color: 'var(--muted)' }}>İlahiyat Fakültesi</div>
            </div>
            <div style={{
              width: 34, height: 34, borderRadius: '50%',
              background: 'var(--gold)', color: 'var(--navy)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 11, fontWeight: 600, flexShrink: 0,
            }}>
              {student.name.split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase()}
            </div>
          </>
        ) : (
          <>
            <div style={{ textAlign: 'right' }}>
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
