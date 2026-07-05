import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import LoginRegister from './pages/LoginRegister'
import Dashboard from './pages/Dashboard'
import Lessons from './pages/Lessons'
import SRSFlashcards from './pages/SRSFlashcards'
import Exercises from './pages/Exercises'
import Teacher from './pages/Teacher'
import LessonDetail from './pages/LessonDetail'
import ArabicChat from './pages/ArabicChat'
import Landing from './pages/Landing'

function AppLayout({ children }) {
  const [selectedUnit, setSelectedUnit] = useState(null)
  return (
    <div className="app-grid">
      <Sidebar selectedUnit={selectedUnit} onSelectUnit={setSelectedUnit} />
      <Header />
      <main className="app-main" style={{ background: 'var(--cream)', minHeight: 0 }}>
        {children}
      </main>
    </div>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
                      <Route path="/landing" element={<Landing />} />
<Route path="/login" element={<LoginRegister />} />
          <Route path="/" element={localStorage.getItem("token") ? <Navigate to="/lessons" replace /> : <Navigate to="/landing" replace />} />
          <Route path="/lessons"           element={<AppLayout><Lessons /></AppLayout>} />
          <Route path="/lessons/:lessonId" element={<AppLayout><LessonDetail /></AppLayout>} />
          <Route path="/exercises"         element={<AppLayout><Exercises /></AppLayout>} />
          <Route path="/srs"               element={<AppLayout><SRSFlashcards /></AppLayout>} />
          <Route path="/dashboard"         element={<AppLayout><Dashboard /></AppLayout>} />
          <Route path="/teacher"           element={<AppLayout><Teacher /></AppLayout>} />
          <Route path="/chat"              element={<AppLayout><ArabicChat /></AppLayout>} />
          <Route path="*"                  element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}