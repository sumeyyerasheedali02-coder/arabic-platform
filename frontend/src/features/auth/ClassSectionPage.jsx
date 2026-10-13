import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import api from '../../api/client'
import { useAuth } from '../../auth/useAuth'
import BrandMark from '../../components/BrandMark'
import { CenteredSpinner } from '../../components/Spinner'
import ClassSectionField from './ClassSectionField'
import StudentNumberField from './StudentNumberField'
import { isStudentNumber } from './studentNumber'
import LanguageSwitch from './LanguageSwitch'
import { LOGIN_TEXTS } from './texts'

/** Complete missing student number and section together, without asking twice. */
export default function ClassSectionPage() {
  const { student, token, loading, login, logout } = useAuth()
  const [classSection, setClassSection] = useState('')
  const [studentNumber, setStudentNumber] = useState('')
  const [lang, setLang] = useState('ar')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const t = LOGIN_TEXTS[lang]
  const needsNumber = !student?.student_number
  const needsSection = !student?.class_section
  const number = student?.student_number || studentNumber
  const section = student?.class_section || classSection
  const ready = isStudentNumber(number) && !!section

  const saveSection = async event => {
    event.preventDefault()
    if (!ready || saving) return
    setSaving(true)
    setError('')
    try {
      const { data } = await api.patch('/auth/me/profile', {
        student_number: number, ...(needsSection ? { class_section: section } : {}),
      })
      login(token, {
        id: data.student_id, name: data.name,
        is_teacher: !!data.is_teacher, class_section: data.class_section,
        role: data.role, is_admin: !!data.is_admin,
        student_number: data.student_number,
      })
      navigate('/lessons', { replace: true })
    } catch (err) {
      const detail = err.response?.data?.detail
      setError(err.response?.status === 404
        ? t.profileServiceUnavailable
        : typeof detail === 'string' ? detail : t.profileSaveFailed)
    } finally {
      setSaving(false)
    }
  }

  if (!token) return <Navigate to="/login" replace />
  if (loading) return <CenteredSpinner size={36} minHeight="100dvh" />
  if (student?.is_admin) return <Navigate to="/admin" replace />
  if (student?.is_teacher) return <Navigate to="/teacher" replace />
  if (!needsNumber && !needsSection) return <Navigate to="/lessons" replace />

  return (
    <main dir={lang === 'ar' ? 'rtl' : 'ltr'} style={{
      minHeight: '100dvh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: 24, background: 'var(--aq-ivory)', fontFamily: 'var(--aq-font-arabic)',
    }}>
      <div style={{ width: '100%', maxWidth: 420 }}>
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 20 }}>
          <LanguageSwitch lang={lang} onChange={setLang} />
        </div>
        <div style={{
          background: 'var(--aq-card)', border: '1px solid var(--aq-border)',
          borderRadius: 24, padding: '32px 24px', boxShadow: '0 4px 24px rgba(0,0,0,.06)',
        }}>
          <BrandMark size={60} style={{ display: 'block', margin: '0 auto 16px' }} />
          <h1 style={{ fontSize: 24, color: 'var(--aq-navy)', marginBottom: 8 }}>{t.completeProfile}</h1>
          <p style={{ fontSize: 13, color: 'var(--aq-text-muted)', marginBottom: 24 }}>{t.profileDescription}</p>
          <form onSubmit={saveSection}>
            <fieldset disabled={saving} style={{ border: 0, minWidth: 0 }}>
              {needsNumber && <StudentNumberField value={studentNumber}
                onChange={value => { setStudentNumber(value); setError('') }} t={t} />}
              {needsSection && <ClassSectionField value={classSection} onChange={setClassSection} t={t} />}
            </fieldset>
            {error && <p role="alert" style={{ color: '#DC2626', fontSize: 13, marginBottom: 12 }}>{error}</p>}
            <button type="submit" disabled={!ready || saving} style={{
              width: '100%', padding: 14, borderRadius: 14, border: 0,
              background: 'var(--aq-gradient-royal)', color: '#FAF8F3',
              fontSize: 15, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit',
              opacity: !ready || saving ? .6 : 1,
            }}>
              {saving ? t.loading : t.saveProfile}
            </button>
          </form>
          <button type="button" disabled={saving} onClick={() => { logout(); navigate('/login') }} style={{
            display: 'block', margin: '20px auto 0', border: 0, background: 'none',
            color: 'var(--aq-text-muted)', fontFamily: 'inherit', cursor: 'pointer',
          }}>
            {t.back}
          </button>
        </div>
      </div>
    </main>
  )
}
