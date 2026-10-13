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
  const { student } = useAuth()
  return student?.is_teacher ? children : <Navigate to="/dashboard" replace />
}

// "/" opens the lessons for a logged-in student and the landing page for everyone else
function Home() {
  const { token } = useAuth()
  return <Navigate to={token ? '/lessons' : '/landing'} replace />
}

// HashRouter: the static host serves index.html only at the root, so the route
// lives after the # and survives a page reload.
export default function App() {
  return (
    <HashRouter>
      <AuthProvider>
        <Routes>
          <Route path="/landing" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<Home />} />
          {/* Pages inside the app shell. Guests may open all of them except /teacher. */}
          <Route element={<AppLayout />}>
            <Route path="/lessons"           element={<LessonsPage />} />
            <Route path="/lessons/:lessonId" element={<LessonDetailPage />} />
            <Route path="/exercises"         element={<ExercisesPage />} />
            <Route path="/srs"               element={<FlashcardsPage />} />
            <Route path="/dashboard"         element={<DashboardPage />} />
            <Route path="/teacher"           element={<TeacherOnly><TeacherPage /></TeacherOnly>} />
            <Route path="/chat"              element={<ChatPage />} />
          </Route>
          <Route path="*"                  element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </HashRouter>
  )
}
