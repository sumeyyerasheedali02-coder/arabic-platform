import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import { useAuth } from '../../auth/useAuth'
import { StaffContext } from './useStaff'

export default function StaffProvider({ children }) {
  const { student } = useAuth()
  const staff = student?.is_teacher || student?.is_admin
  const sections = useApiData(staff ? `staff-sections:${student.id}` : null,
    () => api.get('/teacher/sections').then(r => r.data))
  return <StaffContext.Provider value={sections}>{children}</StaffContext.Provider>
}
