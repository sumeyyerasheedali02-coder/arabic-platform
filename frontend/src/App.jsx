import { lazy, Suspense } from 'react'
import { HashRouter, Routes, Route, Navigate, useLocation, useParams } from 'react-router-dom'
import { AuthProvider } from './auth/AuthContext'
import { useAuth } from './auth/useAuth'
import { CenteredSpinner } from './components/Spinner'
import AppLayout from './layout/AppLayout'

// Each page is its own chunk, fetched the first time it is opened.
const LandingPage      = lazy(() => import('./features/landing/LandingPage'))
const LoginPage        = lazy(() => import('./features/auth/LoginPage'))
const ClassSectionPage = lazy(() => import('./features/auth/ClassSectionPage'))
const LessonsPage      = lazy(() => import('./features/lessons/LessonsPage'))
const LessonDetailPage = lazy(() => import('./features/lessons/LessonDetailPage'))
const ExercisesPage    = lazy(() => import('./features/exercises/ExercisesPage'))
const SharedWordsPage  = lazy(() => import('./features/sharedWords/SharedWordsPage'))
const FlashcardsPage   = lazy(() => import('./features/srs/FlashcardsPage'))
const DashboardPage    = lazy(() => import('./features/dashboard/DashboardPage'))
const TeacherPage      = lazy(() => import('./features/teacher/TeacherPage'))
const StudentDetailPage = lazy(() => import('./features/teacher/StudentDetailPage'))
const AdminPage        = lazy(() => import('./features/admin/AdminPage'))
const AdminTeachersPage = lazy(() => import('./features/admin/AdminTeachersPage'))
const AdminSectionsPage = lazy(() => import('./features/admin/AdminSectionsPage'))
const AdminAuditPage = lazy(() => import('./features/admin/AdminAuditPage'))
const ContentLibraryPage = lazy(() => import('./features/staff/ContentLibraryPage'))
const ChatPage         = lazy(() => import('./features/chat/ChatPage'))
const AccountPage = lazy(() => import('./features/account/AccountPage'))
const PasswordRecoveryPage = lazy(() => import('./features/account/PasswordRecoveryPage'))

// Admins use their own area; legacy teacher links keep working after the split.
function TeacherOnly({ children }) {
  const { student } = useAuth()
  const { pathname, search } = useLocation()
  if (student?.is_admin) return <Navigate to={pathname.replace('/teacher', '/admin') + search} replace />
  return student?.is_teacher ? children : <Navigate to="/dashboard" replace />
}

function AdminOnly({ children }) {
  const { student } = useAuth()
  return student?.is_admin ? children : <Navigate to="/dashboard" replace />
}

function PersonalProgressOnly({ children }) {
  const { student } = useAuth()
  if (student?.is_admin) return <Navigate to="/admin" replace />
  if (student?.is_teacher) return <Navigate to="/teacher" replace />
  return children
}

function ChatAccess({ children }) {
  const { student } = useAuth()
  if (student?.is_admin) return <Navigate to="/admin" replace />
  return student?.is_teacher ? <Navigate to="/teacher" replace /> : children
}

function StaffOnly({ children }) {
  const { student } = useAuth()
  return student?.is_teacher || student?.is_admin ? children : <Navigate to="/lessons" replace />
}

function LearningRoute({ children, exercises = false }) {
  const { student } = useAuth()
  const { lessonId } = useParams()
  if (student?.is_teacher || student?.is_admin) return <Navigate to={lessonId
    ? `/content/lessons/${lessonId}` : exercises ? '/content?tab=exercises' : '/content'} replace />
  return children
}

// "/" opens the lessons for a logged-in student and the landing page for everyone else
function Home() {
  const { token, student, loading } = useAuth()
  if (loading) return <CenteredSpinner size={36} minHeight="100dvh" />
  return <Navigate to={!token ? '/landing' : student?.is_admin ? '/admin'
    : student?.is_teacher ? '/teacher' : '/lessons'} replace />
}

// HashRouter: the static host serves index.html only at the root, so the route
// lives after the # and survives a page reload.
export default function App() {
  return (
    <HashRouter>
      <AuthProvider>
        <Suspense fallback={<CenteredSpinner size={36} minHeight="100vh" background="var(--cream)" />}>
        <Routes>
          <Route path="/landing" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/forgot-password" element={<PasswordRecoveryPage />} />
          <Route path="/reset-password" element={<PasswordRecoveryPage reset />} />
          <Route path="/choose-section" element={<ClassSectionPage />} />
          <Route path="/complete-profile" element={<ClassSectionPage />} />
          <Route path="/" element={<Home />} />
          {/* Shared shell; role guards keep staff pages separate from student pages. */}
          <Route element={<AppLayout />}>
            <Route path="/account" element={<AccountPage />} />
            <Route path="/lessons"           element={<LearningRoute><LessonsPage /></LearningRoute>} />
            <Route path="/lessons/:lessonId" element={<LearningRoute><LessonDetailPage /></LearningRoute>} />
            <Route path="/exercises"         element={<LearningRoute exercises><ExercisesPage /></LearningRoute>} />
            <Route path="/shared-words"      element={<SharedWordsPage />} />
            <Route path="/srs"               element={<PersonalProgressOnly><FlashcardsPage /></PersonalProgressOnly>} />
            <Route path="/dashboard"         element={<PersonalProgressOnly><DashboardPage /></PersonalProgressOnly>} />
            <Route path="/teacher"           element={<TeacherOnly><TeacherPage /></TeacherOnly>} />
            <Route path="/teacher/students" element={<TeacherOnly><TeacherPage view="students" /></TeacherOnly>} />
            <Route path="/teacher/students/:studentId" element={<TeacherOnly><StudentDetailPage /></TeacherOnly>} />
            <Route path="/admin" element={<AdminOnly><AdminPage /></AdminOnly>} />
            <Route path="/admin/teachers" element={<AdminOnly><AdminTeachersPage /></AdminOnly>} />
            <Route path="/admin/sections" element={<AdminOnly><AdminSectionsPage /></AdminOnly>} />
            <Route path="/admin/students" element={<AdminOnly><TeacherPage view="students" /></AdminOnly>} />
            <Route path="/admin/students/:studentId" element={<AdminOnly><StudentDetailPage /></AdminOnly>} />
            <Route path="/admin/audit" element={<AdminOnly><AdminAuditPage /></AdminOnly>} />
            <Route path="/content" element={<StaffOnly><ContentLibraryPage /></StaffOnly>} />
            <Route path="/content/lessons/:lessonId" element={<StaffOnly><LessonDetailPage /></StaffOnly>} />
            <Route path="/chat"              element={<ChatAccess><ChatPage /></ChatAccess>} />
          </Route>
          <Route path="*"                  element={<Navigate to="/" replace />} />
        </Routes>
        </Suspense>
      </AuthProvider>
    </HashRouter>
  )
}
