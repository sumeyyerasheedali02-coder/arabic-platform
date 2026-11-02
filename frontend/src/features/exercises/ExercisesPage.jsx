import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import { useAuth } from '../../auth/useAuth'
import ErrorState from '../../components/ErrorState'
import { CenteredSpinner } from '../../components/Spinner'
import { useUnits } from '../units/useUnits'
import PracticeWorkspace from './PracticeWorkspace'
import './practice.css'

export default function ExercisesPage() {
  const { token, student } = useAuth()
  const { units, selectedUnit, loading, error, reload } = useUnits()
  // Unit selection is still shared with lessons and the sidebar.
  const unitId = selectedUnit?.id
  const query = useApiData(unitId == null ? null : `exercises:${unitId}`,
    () => api.get(`/units/${unitId}/exercises`).then(r => r.data))

  if (loading) return <CenteredSpinner size={32} height={260} />
  if (error && !units.length) return <ErrorState onRetry={reload} />
  return (
    <div className="practice-page">
      <header className="practice-page-header">
        <div><span className="practice-eyebrow">مساحة التدريب</span><h1>التدريبات</h1><p>{selectedUnit?.title_ar}</p></div>
      </header>
      {query.loading ? <CenteredSpinner size={28} height={200} /> : query.error ? <ErrorState onRetry={query.reload} />
        : selectedUnit && <PracticeWorkspace key={`${student?.id ?? 'guest'}:${unitId}`}
          unit={selectedUnit} allExercises={query.data ?? []} isGuest={!token} />}
    </div>
  )
}
