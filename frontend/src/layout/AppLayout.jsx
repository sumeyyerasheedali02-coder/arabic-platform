import { useState } from 'react'
import { useLocation } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'

/** Sidebar + header + scrolling main area shared by every page inside the app. */
export default function AppLayout({ children }) {
  const [selectedUnit, setSelectedUnit] = useState(null)
  // Mobile: the sidebar is a slide-in drawer opened from the header menu button
  const [menuOpen, setMenuOpen] = useState(false)
  const location = useLocation()
  const [menuPath, setMenuPath] = useState(location.pathname)
  if (menuPath !== location.pathname) {   // close the drawer after navigating
    setMenuPath(location.pathname)
    setMenuOpen(false)
  }
  return (
    <div className="app-grid">
      <Sidebar selectedUnit={selectedUnit} onSelectUnit={setSelectedUnit} open={menuOpen} />
      {menuOpen && <div className="sidebar-backdrop" onClick={() => setMenuOpen(false)} />}
      <Header onMenuClick={() => setMenuOpen(v => !v)} />
      <main className="app-main" style={{ background: 'var(--cream)', minHeight: 0 }}>
        {children}
      </main>
    </div>
  )
}
