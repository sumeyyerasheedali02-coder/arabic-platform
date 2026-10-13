import api from '../../api/client'
import { useStaffApiData } from '../staff/useStaffApiData'
import { useAuth } from '../../auth/useAuth'
import { CenteredSpinner } from '../../components/Spinner'
import { useStaff } from '../staff/useStaff'
import { StaffMessage } from '../teacher/StaffUi'
import { apiError } from '../teacher/staffFormat'
import SectionCards from './SectionCards'

export default function AdminSectionsPage() {
  const { student } = useAuth()
  const sections = useStaff()
  const teachers = useStaffApiData(`section-teachers:${student.id}`,
    () => api.get('/admin/teachers').then(r => r.data))
  function refresh() { sections.reload(); teachers.reload() }
  if (sections.loading || teachers.loading) return <CenteredSpinner size={32} height={260} />
  return <div className="staff-page" dir="rtl">
    <div className="staff-toolbar"><h1>الشُّعَب</h1></div>
    <p className="staff-intro">توزيع الطلاب والمدرسين على شُعَب التحضيري العربي.</p>
    {sections.error || teachers.error
      ? <StaffMessage error={apiError(sections.error || teachers.error)} onRetry={refresh} />
      : <SectionCards sections={sections.data ?? []} teachers={teachers.data ?? []} />}
  </div>
}
