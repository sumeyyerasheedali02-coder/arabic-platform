import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import { apiError } from '../teacher/staffFormat'
import BrandMark from '../../components/BrandMark'
import './account.css'

export default function PasswordRecoveryPage({ reset = false }) {
  const location = useLocation()
  const token = new URLSearchParams(location.search).get('token') || ''
  const availability = useApiData(reset ? null : 'password-recovery-status',
    () => api.get('/account/recovery-status').then(r => r.data))
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmation, setConfirmation] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  async function submit(event) {
    event.preventDefault(); setError(''); setMessage('')
    if (reset && password !== confirmation) { setError('كلمتا المرور غير متطابقتين'); return }
    if (reset && new TextEncoder().encode(password).length > 72) { setError('كلمة المرور طويلة جدًا'); return }
    setBusy(true)
    try {
      const { data } = await api.post(reset ? '/account/reset-password' : '/account/forgot-password',
        reset ? { token, password } : { email })
      setMessage(data.message)
      setPassword(''); setConfirmation('')
    } catch (err) { setError(apiError(err)) }
    finally { setBusy(false) }
  }
  return <main className="account-recovery" dir="rtl"><section className="account-panel">
    <BrandMark size={84} />
    <h1>{reset ? 'تعيين كلمة مرور جديدة' : 'استعادة كلمة المرور'}</h1>
    {message ? <p className="account-success" role="status">{message}</p>
      : !reset && availability.loading ? <p role="status">جارٍ التحقق من خدمة الاستعادة…</p>
      : !reset && availability.error ? <p role="alert">{apiError(availability.error)}</p>
      : !reset && !availability.data?.enabled
        ? <p className="account-hint">استعادة كلمة المرور بالبريد غير مفعّلة بعد. تواصل مع إدارة المنصة للمساعدة.</p>
      : reset && !token
      ? <p role="alert">رابط الاستعادة غير مكتمل. اطلب رابطًا جديدًا.</p>
      : <form onSubmit={submit}>
        {reset ? <>
          <label htmlFor="recovery-password">كلمة المرور الجديدة</label>
          <input id="recovery-password" type="password" required minLength={8} maxLength={72} autoComplete="new-password"
            value={password} onChange={e => setPassword(e.target.value)} disabled={busy} />
          <label htmlFor="recovery-confirm">تأكيد كلمة المرور</label>
          <input id="recovery-confirm" type="password" required autoComplete="new-password"
            value={confirmation} onChange={e => setConfirmation(e.target.value)} disabled={busy} />
        </> : <>
          <p className="account-hint">أدخل البريد المرتبط بحسابك لإرسال رابط استعادة كلمة المرور.</p>
          <label htmlFor="recovery-email">البريد الإلكتروني</label>
          <input id="recovery-email" type="email" autoComplete="email" required dir="ltr"
            value={email} onChange={e => setEmail(e.target.value)} disabled={busy} />
        </>}
        {error && <p className="account-error" role="alert">{error}</p>}
        <button disabled={busy}>{busy ? 'جارٍ الإرسال…' : reset ? 'حفظ كلمة المرور' : 'إرسال رابط الاستعادة'}</button>
      </form>}
    <Link to="/login">العودة لتسجيل الدخول</Link>
    {reset && !token && <Link to="/forgot-password">طلب رابط جديد</Link>}
  </section></main>
}
