import { Suspense, useCallback, useEffect, useRef, useState } from 'react'
import { Link, Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../auth/useAuth'
import { CenteredSpinner } from '../components/Spinner'
import { ProgressProvider } from '../features/progress/ProgressProvider'
import { UnitsProvider } from '../features/units/UnitsProvider'
import StaffProvider from '../features/staff/StaffProvider'
import Header from './Header'
import Sidebar from './Sidebar'
import ActivityTracker from '../features/activity/ActivityTracker'
import { usePhoneLayout } from '../components/useMediaQuery'
import { useOverlayFocus } from '../components/useOverlayFocus'

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
  const phone = usePhoneLayout()
  const sidebarRef = useRef(null)
  const closeMenu = useCallback(() => setMenuOpen(false), [])
  const drawerOpen = phone && menuOpen
  useOverlayFocus(sidebarRef, drawerOpen, closeMenu, '.app-header, .app-main')
  useEffect(() => {
    // Safari's virtual keyboard shrinks the visual viewport, not always 100dvh.
    const viewport = window.visualViewport
    if (!viewport || !phone) return
    const update = () => {
      // Pinch zoom must magnify the existing layout, not make it collapse.
      if (Math.abs(viewport.scale - 1) < 0.01) {
        document.documentElement.style.setProperty('--app-visible-height', `${viewport.height}px`)
      }
    }
    update()
    viewport.addEventListener('resize', update)
    return () => {
      viewport.removeEventListener('resize', update)
      document.documentElement.style.removeProperty('--app-visible-height')
    }
  }, [phone])
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
          <Sidebar open={drawerOpen} phone={phone} sidebarRef={sidebarRef} onNavigate={closeMenu} />
          {drawerOpen && <div className="sidebar-backdrop" onClick={closeMenu} aria-hidden="true" />}
          <Header menuOpen={drawerOpen} onMenuClick={() => setMenuOpen(v => !v)} />
          <main className="app-main" style={{ background: 'var(--cream)', minHeight: 0 }}>
            {/* The shell stays on screen while the next page's code loads */}
            <Suspense fallback={<CenteredSpinner size={32} height={260} />}>
              <Outlet />
            </Suspense>
          </main>
          {token && student && !isStaff && location.pathname !== '/chat' && !drawerOpen &&
            <Link to="/chat" className={`ai-floating-link${location.pathname === '/exercises' ? ' ai-floating-link-practice' : ''}`} aria-label="فتح محادثة AI" title="محادثة AI">
              <svg viewBox="0 0 24 24" width="25" height="25" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M21 11a8 8 0 0 1-8 8H7l-4 3V11a8 8 0 0 1 8-8h2a8 8 0 0 1 8 8Z" /><path d="m12 7 1 3 3 1-3 1-1 3-1-3-3-1 3-1 1-3Z" /></svg>
              <span>محادثة AI</span>
            </Link>}
        </div>
      </ProgressProvider>
    </UnitsProvider>
    </StaffProvider>
  )
}
