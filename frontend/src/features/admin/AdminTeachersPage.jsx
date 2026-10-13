import { useState } from 'react'
import api from '../../api/client'
import { useStaffApiData } from '../staff/useStaffApiData'
import { useAuth } from '../../auth/useAuth'
import { CenteredSpinner } from '../../components/Spinner'
import { useStaff } from '../staff/useStaff'
import { StaffMessage } from '../teacher/StaffUi'
import { apiError } from '../teacher/staffFormat'
import TeacherForm from './TeacherForm'

export default function AdminTeachersPage() {
  const { student } = useAuth()
  const sections = useStaff()
  const [editing, setEditing] = useState(null)
  const [notice, setNotice] = useState('')
  const data = useStaffApiData(`admin-teachers:${student.id}`,
    () => api.get('/admin/teachers').then(r => r.data))
  function saved(message) {
    setEditing(null); setNotice(message); data.reload(); sections.reload()
  }
  return <div className="staff-page" dir="rtl">
    <h1>المدرسون</h1>
    <p className="staff-intro">أنشئ حسابات المدرسين، وأسند الشُّعَب، وأدِر حالة الحساب وكلمة المرور.</p>
    {data.loading ? <CenteredSpinner size={32} height={260} />
      : data.error ? <StaffMessage error={apiError(data.error)} onRetry={data.reload} />
      : <>
        {notice && <div role="status" className="staff-success">{notice}</div>}
        {editing && <TeacherForm key={editing.id || 'new'} teacher={editing.id ? editing : null}
          onSaved={saved} onCancel={() => setEditing(null)} />}
        <section className="staff-panel">
          <div className="staff-toolbar"><h2>حسابات المدرسين</h2>
            <button className="staff-primary" onClick={() => { setEditing({}); setNotice('') }}>إضافة أستاذ</button>

          </div>
          <div className="staff-table-wrap"><table className="staff-table">
            <thead><tr>{['الأستاذ','الشُّعَب','الحالة',''].map((h,i) => <th key={i}>{h}</th>)}</tr></thead>
            <tbody>{(data.data ?? []).map(t => <tr key={t.id}>
              <td>{t.name}<div className="staff-secondary" dir="ltr">{t.email}</div></td>
              <td>{t.sections.length ? t.sections.join('، ') : 'لم تُسند شعبة بعد'}</td>
              <td><span className={`staff-badge ${t.is_active ? '' : 'inactive'}`}>{t.is_active ? 'نشط' : 'معطّل'}</span></td>
              <td><button onClick={() => { setEditing(t); setNotice('') }} aria-label={`إدارة حساب ${t.name}`}>إدارة الحساب</button></td>
            </tr>)}
            {!data.data?.length && <tr><td className="staff-empty" colSpan={4}>
              لا يوجد مدرسون بعد. أضف أستاذًا وحدّد الشُّعَب المسندة إليه.
            </td></tr>}
            </tbody>
          </table></div>
        </section>
      </>}
  </div>
}
