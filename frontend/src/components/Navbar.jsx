import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const navLinks = [
  { to: '/',          label: 'الرئيسية',    icon: '🏠' },
  { to: '/lessons',   label: 'الدروس',       icon: '📖' },
  { to: '/exercises', label: 'التمارين',     icon: '✏️' },
  { to: '/srs',       label: 'البطاقات',     icon: '🗂️' },
]

export default function Navbar() {
  const { student, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()

  const handleLogout = () => { logout(); navigate('/login') }

  return (
    <nav className="fixed top-0 right-0 left-0 z-50 bg-dark-surface/95 backdrop-blur-md border-b border-dark-border shadow-lg">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2">
          <span className="text-xl">📚</span>
          <span className="font-bold text-white text-base leading-tight hidden sm:block">
            العربية بين يديك
          </span>
        </Link>

        {/* Nav links */}
        <div className="flex items-center gap-0.5">
          {navLinks.map(({ to, label, icon }) => {
            const active = location.pathname === to
            return (
              <Link
                key={to}
                to={to}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                  active
                    ? 'bg-primary-600/20 text-primary-400'
                    : 'text-slate-400 hover:bg-dark-elevated hover:text-white'
                }`}
              >
                <span>{icon}</span>
                <span className="hidden md:inline">{label}</span>
              </Link>
            )
          })}
          <Link
            to="/chat"
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 ${
              location.pathname === '/chat'
                ? 'bg-primary-600/20 text-primary-400'
                : 'text-slate-400 hover:bg-dark-elevated hover:text-white'
            }`}
          >
            <span>🤖</span>
            <span className="hidden md:inline">المساعد الذكي</span>
          </Link>
        </div>

        {/* Student info + teacher link + logout */}
        <div className="flex items-center gap-3">
          {student && (
            <span className="text-sm text-slate-500 hidden sm:block">
              <span className="font-semibold text-primary-400">{student.name}</span>
            </span>
          )}
          <Link
            to="/teacher"
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 ${
              location.pathname === '/teacher'
                ? 'bg-amber-500/20 text-amber-400'
                : 'text-slate-600 hover:bg-dark-elevated hover:text-slate-300'
            }`}
            title="لوحة المعلم"
          >
            <span>🎓</span>
            <span className="hidden lg:inline">المعلم</span>
          </Link>
          <button
            onClick={handleLogout}
            className="text-sm px-3 py-1.5 rounded-lg border border-red-800/40 text-red-400 hover:bg-red-400/10 transition-colors font-medium"
          >
            خروج
          </button>
        </div>
      </div>
    </nav>
  )
}
