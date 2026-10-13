import { useState } from 'react'
import api from '../../api/client'
import { StaffMessage } from '../teacher/StaffUi'
import { apiError } from '../teacher/staffFormat'

export default function TeacherForm({ teacher, onSaved, onCancel }) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [sections, setSections] = useState(teacher?.sections ?? [])
  const [active, setActive] = useState(teacher?.is_active ?? true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  function toggle(section) {
    setSections(prev => prev.includes(section) ? prev.filter(s => s !== section) : [...prev, section])
  }
  async function save(event) {
    event.preventDefault()
    if (active && !sections.length) { setError('اختر شعبة واحدة على الأقل.'); return }
    setError(''); setSaving(true)
    try {
      if (teacher) await api.patch(`/admin/teachers/${teacher.id}`, {
        sections, is_active: active, password: password || null,
      })
      else await api.post('/admin/teachers', { name, email, password, sections })
      setPassword('')
      onSaved(teacher ? 'حُفظت إعدادات الأستاذ.' : 'أُنشئ حساب الأستاذ. يمكنه الدخول بالبريد وكلمة المرور المحددين.')
    } catch (err) { setError(apiError(err)) }
    finally { setSaving(false) }
  }
  return <section className="staff-panel">
    <h2>{teacher ? `إدارة حساب ${teacher.name}` : 'إضافة أستاذ'}</h2>
    {teacher && <p className="staff-intro" dir="ltr">{teacher.email}</p>}
    <form onSubmit={save} className="staff-form">
      <fieldset disabled={saving}>
        <div className="staff-form-grid">
          {!teacher && <>
            <label className="staff-field">اسم الأستاذ
              <input required maxLength={120} value={name} onChange={e => setName(e.target.value)} autoComplete="name" />
            </label>
            <label className="staff-field">البريد الإلكتروني
              <input required type="email" dir="ltr" value={email} onChange={e => setEmail(e.target.value)} autoComplete="off" />
            </label>
          </>}
          <label className="staff-field">{teacher ? 'كلمة مرور جديدة · اختياري' : 'كلمة المرور'}
            <input required={!teacher} type="password" minLength={10} dir="ltr"
              value={password} onChange={e => setPassword(e.target.value)} autoComplete="new-password" />
          </label>
        </div>
        <p className="staff-intro" style={{ margin: '12px 0' }}>
          {teacher ? 'تغيير كلمة المرور أو تعطيل الحساب ينهي جلساته الحالية.' :
            'استخدم 10 أحرف على الأقل، وأبلغ الأستاذ بكلمة المرور عبر وسيلة خاصة. لا تُرسل المنصة بريدًا تلقائيًا.'}
        </p>
        <fieldset><legend>الشُّعَب المسندة إليه</legend>
          <div className="staff-section-choices">{['A','B','C','D'].map(s => <label key={s}>
            <input type="checkbox" checked={sections.includes(s)} onChange={() => toggle(s)} />
            الشعبة {s}
          </label>)}</div>
        </fieldset>
        {teacher && <label><input type="checkbox" checked={active}
          onChange={e => setActive(e.target.checked)} /> الحساب نشط</label>}
        {error && <StaffMessage error={error} />}
        <div className="staff-actions">
          <button type="submit" className="staff-primary">{saving ? 'جارٍ الحفظ…' : teacher ? 'حفظ التغييرات' : 'إنشاء حساب الأستاذ'}</button>
          <button type="button" onClick={onCancel}>إلغاء</button>
        </div>
      </fieldset>
    </form>
  </section>
}
