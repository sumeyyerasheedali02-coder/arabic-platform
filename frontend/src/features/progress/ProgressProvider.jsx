import { useMemo } from 'react'
import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import { useAuth } from '../../auth/useAuth'
import { ProgressContext } from './useProgress'

const NO_PROGRESS = []

export function ProgressProvider({ children }) {
  const { student, token } = useAuth()
  // Keyed by student so one account never sees another account's rows
  const key = token && student && !student.is_teacher && !student.is_admin ? `progress:${student.id}` : null
  const { data, loading, error, reload } = useApiData(key, () => api.get('/me/progress').then(r => r.data))

  const value = useMemo(
    () => ({ progress: data ?? NO_PROGRESS, loading, error, reload }),
    [data, loading, error, reload],
  )
  return <ProgressContext.Provider value={value}>{children}</ProgressContext.Provider>
}
