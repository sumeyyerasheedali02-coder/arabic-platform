import { HashRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './auth/AuthContext'
import { useAuth } from './auth/useAuth'
import AppLayout from './layout/AppLayout'
import LandingPage from './features/landing/LandingPage'
import LoginPage from './features/auth/LoginPage'
import LessonsPage from './features/lessons/LessonsPage'
import LessonDetailPage from './features/lessons/LessonDetailPage'
import ExercisesPage from './features/exercises/ExercisesPage'
import FlashcardsPage from './features/srs/FlashcardsPage'
import DashboardPage from './features/dashboard/DashboardPage'
import TeacherPage from './features/teacher/TeacherPage'
import ChatPage from './features/chat/ChatPage'

// Students are sent to their own progress page; only the teacher reaches /teacher
// (the backend enforces this too — this only avoids showing an empty page)
function TeacherOnly({ children }) {
  const { student, loading } = useAuth()
  if (loading) return null
  return student?.is_teacher ? children : <Navigate to="/dashboard" replace />
}

// HashRouter: the static host serves index.html only at the root, so the route
// lives after the # and survives a page reload.
export default function App() {
  return (
    <AuthProvider>
      <HashRouter>
        <Routes>
          <Route path="/landing" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={localStorage.getItem('token') ? <Navigate to="/lessons" replace /> : <Navigate to="/landing" replace />} />
          <Route path="/lessons"           element={<AppLayout><LessonsPage /></AppLayout>} />
          <Route path="/lessons/:lessonId" element={<AppLayout><LessonDetailPage /></AppLayout>} />
          <Route path="/exercises"         element={<AppLayout><ExercisesPage /></AppLayout>} />
          <Route path="/srs"               element={<AppLayout><FlashcardsPage /></AppLayout>} />
          <Route path="/dashboard"         element={<AppLayout><DashboardPage /></AppLayout>} />
          <Route path="/teacher"           element={<TeacherOnly><AppLayout><TeacherPage /></AppLayout></TeacherOnly>} />
          <Route path="/chat"              element={<AppLayout><ChatPage /></AppLayout>} />
          <Route path="*"                  element={<Navigate to="/" replace />} />
        </Routes>
      </HashRouter>
    </AuthProvider>
  )
}
