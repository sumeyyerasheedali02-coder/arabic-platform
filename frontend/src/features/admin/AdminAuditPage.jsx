import { Link, useSearchParams } from 'react-router-dom'
import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import { useAuth } from '../../auth/useAuth'
import { CenteredSpinner } from '../../components/Spinner'
import { StaffMessage } from '../teacher/StaffUi'
import { apiError, formatDateTime } from '../teacher/staffFormat'

const ACTIONS = {
  teacher_created: 'إنشاء حساب أستاذ',
  teacher_updated: 'تعديل حساب أستاذ',
  student_section_changed: 'تصحيح شعبة طالب',
}
const sectionText = list => list?.length ? list.join('، ') : 'لا توجد'
function describe(item) {
  const d = item.details
  if (item.action === 'teacher_created') return `الشُّعَب: ${sectionText(d.sections)}`
  if (item.action === 'student_section_changed') return `الشعبة: ${d.previous_section || 'غير محددة'} ← ${d.class_section}`
  return `الشُّعَب: ${sectionText(d.previous_sections)} ← ${sectionText(d.sections)} · ${d.is_active ? 'الحساب نشط' : 'الحساب معطّل'}${d.password_reset ? ' · أُعيد تعيين كلمة المرور' : ''}`
}

export default function AdminAuditPage() {
  const { student } = useAuth()
  const [params, setParams] = useSearchParams()
  const action = params.get('action') || ''
  const rawOffset = Number(params.get('offset'))
  const offset = Number.isInteger(rawOffset) && rawOffset >= 0 ? rawOffset : 0
  const log = useApiData(`audit:${student.id}:${action}:${offset}`,
    () => api.get('/admin/audit', { params: { offset, limit: 25, ...(action ? { action } : {}) } }).then(r => r.data))
  function change(nextOffset, nextAction = action) {
    setParams({ ...(nextOffset ? { offset: String(nextOffset) } : {}), ...(nextAction ? { action: nextAction } : {}) })
  }
  return <div className="staff-page" dir="rtl">
    <h1>سجل الإدارة</h1>
    <p className="staff-intro">تغييرات حسابات المدرسين والشُّعَب، مع اسم من أجرى التغيير ووقته.</p>
    <div className="staff-toolbar">
      <label htmlFor="audit-action">نوع العملية</label>
      <select id="audit-action" value={action} onChange={e => change(0, e.target.value)}>
        <option value="">جميع العمليات</option>
        {Object.entries(ACTIONS).map(([key,label]) => <option key={key} value={key}>{label}</option>)}
      </select>
      <button onClick={log.reload}>تحديث</button>
    </div>
    {log.loading ? <CenteredSpinner size={30} height={240} />
      : log.error ? <StaffMessage error={apiError(log.error)} onRetry={log.reload} />
      : <section className="staff-panel">
        <div className="staff-table-wrap"><table className="staff-table">
          <thead><tr>{['العملية','الحساب المعني','التفاصيل','أجراها','الوقت'].map(h => <th key={h}>{h}</th>)}</tr></thead>
          <tbody>{(log.data?.items ?? []).map(item => <tr key={item.id}>
            <td>{ACTIONS[item.action] || item.action}</td>
            <td><Link to={item.target_role === 'student'
              ? `/admin/students/${item.target_id}` : '/admin/teachers'}>{item.target_name}</Link></td>
            <td>{describe(item)}</td><td>{item.actor_name}</td><td>{formatDateTime(item.created_at)}</td>
          </tr>)}
          {!log.data?.items.length && <tr><td colSpan={5} className="staff-empty">
            لا توجد عمليات مطابقة. ستظهر تغييرات الإدارة هنا عند إجرائها.
          </td></tr>}
          </tbody>
        </table></div>
        <div className="staff-toolbar staff-pagination">
          <button disabled={offset === 0} onClick={() => change(Math.max(0, offset - 25))}>السابق</button>
          <span>{log.data?.total ? `${offset + 1}–${Math.min(offset + 25, log.data.total)} من ${log.data.total}` : '0 عملية'}</span>
          <button disabled={offset + 25 >= (log.data?.total ?? 0)} onClick={() => change(offset + 25)}>التالي</button>
        </div>
      </section>}
  </div>
}
