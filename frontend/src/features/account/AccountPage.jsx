import { useState } from 'react'
import { Navigate } from 'react-router-dom'
import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import { useAuth } from '../../auth/useAuth'
import { CenteredSpinner } from '../../components/Spinner'
import { StaffMessage } from '../teacher/StaffUi'
import { apiError } from '../teacher/staffFormat'
import './account.css'

function AccountForms({ profile }) {
  const { login, student } = useAuth()
  const [name, setName] = useState(profile.name)
  const [savedName, setSavedName] = useState(profile.name)
  const [currentPassword, setCurrentPassword] = useState('')
  const [password, setPassword] = useState('')
  const [confirmation, setConfirmation] = useState('')
  const [busy, setBusy] = useState('')
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  async function save(event, kind) {
    event.preventDefault()
    setError(''); setNotice('')
    if (kind === 'password' && password !== confirmation) {
      setError('كلمتا المرور غير متطابقتين'); return
    }
    if (kind === 'password' && new TextEncoder().encode(password).length > 72) {
      setError('كلمة المرور طويلة جدًا'); return
    }
    setBusy(kind)
    try {
      const { data } = kind === 'name'
        ? await api.patch('/account/me', { name: name.trim() })
        : await api.post('/account/password', { current_password: currentPassword, password })
      login(data.access_token, { ...student, name: data.name })
      if (kind === 'name') setSavedName(data.name)
      setNotice(kind === 'name' ? 'تم حفظ الاسم.' : 'تم تغيير كلمة المرور وإنهاء الجلسات الأخرى في المنصتين.')
      if (kind === 'password') { setCurrentPassword(''); setPassword(''); setConfirmation('') }
    } catch (err) { setError(apiError(err)) }
    finally { setBusy('') }
  }

  return <div className="account-page" dir="rtl">
    <h1>إعدادات الحساب</h1>
    {notice && <p className="account-success" role="status">{notice}</p>}
    {error && <StaffMessage error={error} />}
    <section className="account-panel">
      <h2>المعلومات الشخصية</h2>
      <form onSubmit={e => save(e, 'name')}>
        <label htmlFor="account-name">الاسم</label>
        <input id="account-name" value={name} onChange={e => setName(e.target.value)}
          autoComplete="name" required minLength={2} maxLength={100} disabled={!!busy} />
        <label htmlFor="account-email">البريد الإلكتروني</label>
        <input id="account-email" value={profile.email} readOnly dir="ltr" />
        {profile.role === 'student' && <p className="account-hint">
          رقم الطالب: {profile.student_number || 'لم يُحدد'} · الشعبة: {profile.class_section || 'لم تُحدد'}.
          لتصحيح الرقم أو الشعبة، تواصل مع الإدارة.
        </p>}
        <p className="account-hint">تغيير البريد يحتاج تأكيد ملكيته؛ هذه الخدمة ستُتاح عند تفعيل البريد.</p>
        <button disabled={!!busy || name.trim() === savedName || name.trim().length < 2}>
          {busy === 'name' ? 'جارٍ الحفظ…' : 'حفظ الاسم'}
        </button>
      </form>
    </section>
    <section className="account-panel">
      <h2>تغيير كلمة المرور</h2>
      <form onSubmit={e => save(e, 'password')}>
        <label htmlFor="current-password">كلمة المرور الحالية</label>
        <input id="current-password" type="password" autoComplete="current-password" required
          value={currentPassword} onChange={e => setCurrentPassword(e.target.value)} disabled={!!busy} />
        <label htmlFor="new-password">كلمة المرور الجديدة</label>
        <input id="new-password" type="password" autoComplete="new-password" minLength={8} maxLength={72} required
          value={password} onChange={e => setPassword(e.target.value)} disabled={!!busy} />
        <label htmlFor="confirm-password">تأكيد كلمة المرور الجديدة</label>
        <input id="confirm-password" type="password" autoComplete="new-password" required
          value={confirmation} onChange={e => setConfirmation(e.target.value)} disabled={!!busy} />
        <p className="account-hint">8 أحرف على الأقل. سيؤدي التغيير إلى إنهاء جلساتك الأخرى، بما فيها منصة العلامات.</p>
        <button disabled={!!busy}>{busy === 'password' ? 'جارٍ الحفظ…' : 'تغيير كلمة المرور'}</button>
      </form>
    </section>
  </div>
}

export default function AccountPage() {
  const { student, token } = useAuth()
  const profile = useApiData(token ? `account:${student.id}` : null,
    () => api.get('/account/me').then(r => r.data))
  if (!token) return <Navigate to="/login" replace />
  if (profile.loading) return <CenteredSpinner />
  if (profile.error) return <div className="account-page"><StaffMessage error={apiError(profile.error)} onRetry={profile.reload} /></div>
  return profile.data ? <AccountForms key={student.id} profile={profile.data} /> : null
}
