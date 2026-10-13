import api from '../../api/client'
import { useLocation } from 'react-router-dom'
import { useStaffApiData } from './useStaffApiData'
import { useAuth } from '../../auth/useAuth'
import { StaffContext } from './useStaff'

export default function StaffProvider({ children }) {
  const { student } = useAuth()
  const { pathname } = useLocation()
  const staff = student?.is_teacher || student?.is_admin
  const sections = useStaffApiData(staff ? `staff-sections:${student.id}:${pathname}` : null,
    () => api.get('/teacher/sections').then(r => r.data))
  return <StaffContext.Provider value={sections}>{children}</StaffContext.Provider>
}
