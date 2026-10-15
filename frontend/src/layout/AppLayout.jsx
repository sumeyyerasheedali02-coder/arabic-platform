import { Suspense, useState } from 'react'
import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../auth/useAuth'
import { CenteredSpinner } from '../components/Spinner'
import { ProgressProvider } from '../features/progress/ProgressProvider'
import { UnitsProvider } from '../features/units/UnitsProvider'
import StaffProvider from '../features/staff/StaffProvider'
import Header from './Header'
import Sidebar from './Sidebar'
import ActivityTracker from '../features/activity/ActivityTracker'

/**
 * Sidebar + header + scrolling main area shared by every page inside the app.
 * It also owns the data those pages share (units, selected unit, progress), so
 * it is loaded once and not again on every navigation.
 */
export default function AppLayout() {
  const { student, token, loading } = useAuth()
  const isStaff = student?.is_teacher || student?.is_admin
  // Mobile: the sidebar is a slide-in drawer opened from the header menu button
  const [menuOpen, setMenuOpen] = useState(false)
  const location = useLocation()
  const [menuPath, setMenuPath] = useState(location.pathname)
  if (menuPath !== location.pathname) {   // close the drawer after navigating
    setMenuPath(location.pathname)
    setMenuOpen(false)
  }
  if (loading) return <CenteredSpinner size={36} minHeight="100dvh" />
  if (token && !isStaff && (!student?.class_section || !student?.student_number)) {
    return <Navigate to="/complete-profile" replace />
  }
  return (
    <StaffProvider>
    <ActivityTracker />
    <UnitsProvider active={!isStaff || location.pathname.startsWith('/content')}>
      <ProgressProvider>
        <div className="app-grid">
          <Sidebar open={menuOpen} onNavigate={() => setMenuOpen(false)} />
          {menuOpen && <div className="sidebar-backdrop" onClick={() => setMenuOpen(false)} />}
          <Header onMenuClick={() => setMenuOpen(v => !v)} />
          <main className="app-main" style={{ background: 'var(--cream)', minHeight: 0 }}>
            {/* The shell stays on screen while the next page's code loads */}
            <Suspense fallback={<CenteredSpinner size={32} height={260} />}>
              <Outlet />
            </Suspense>
          </main>
        </div>
      </ProgressProvider>
    </UnitsProvider>
    </StaffProvider>
  )
}
