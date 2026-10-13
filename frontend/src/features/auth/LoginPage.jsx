import { useState, useRef } from 'react'
import { useLocation, useNavigate, Link } from 'react-router-dom'
import api from '../../api/client'
import BrandMark from '../../components/BrandMark'
import { useAuth } from '../../auth/useAuth'
import CardHeading from './CardHeading'
import ClassSectionField from './ClassSectionField'
import StudentNumberField from './StudentNumberField'
import { isStudentNumber, normalizeStudentNumber } from './studentNumber'
import HeroPanel from './HeroPanel'
import LanguageSwitch from './LanguageSwitch'
import { EMAIL_PATTERN, LOGIN_FAILED, LOGIN_TEXTS, MIN_PASSWORD_LENGTH, PASSWORD_TOO_SHORT } from './texts'

const inputStyle = {
  width: '100%', padding: '14px 18px', borderRadius: 14, boxSizing: 'border-box',
  background: 'var(--aq-ivory)', border: '1.5px solid var(--aq-border)',
  color: 'var(--aq-text)', fontSize: 15, outline: 'none',
  transition: 'border-color .2s, box-shadow .2s',
  fontFamily: "var(--aq-font-sans)",
}
const labelStyle = {
  display: 'block', fontSize: 13, fontWeight: 600,
  color: 'var(--aq-text-muted)', marginBottom: 8,
  fontFamily: "var(--aq-font-arabic)",
}
const fieldIcon = { position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)' }

const highlight = e => { e.target.style.borderColor = '#C9A84C'; e.target.style.boxShadow = '0 0 0 3px rgba(201,168,76,0.12)' }
const unhighlight = e => { e.target.style.borderColor = 'var(--aq-border)'; e.target.style.boxShadow = 'none' }

/**
 * One form for both logging in and registering. The e-mail is looked up first
 * (`emailState`: idle → checking → existing | new), then the matching fields appear.
 */
export default function LoginPage() {
  const [email, setEmail]         = useState('')
  const [emailState, setEmailState] = useState('idle')
  const [name, setName]           = useState('')
  const [password, setPassword]   = useState('')
  const [showPwd, setShowPwd]     = useState(false)
  const [classSection, setClassSection] = useState('')
  const [studentNumber, setStudentNumber] = useState('')
  const [error, setError]         = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [lang, setLang] = useState('ar')
  const passwordRef               = useRef(null)
  const { login }                 = useAuth()
  const navigate                  = useNavigate()
  // Set when the server rejected a stored login and sent the student here
  const sessionExpired            = useLocation().state?.sessionExpired === true

  const t = LOGIN_TEXTS[lang]
  const busy = submitting || emailState === 'checking'

  const handleEmailBlur = async () => {
    const val = email.trim()
    if (isStudentNumber(val)) {
      setEmailState('existing')
      setError('')
      setTimeout(() => passwordRef.current?.focus(), 80)
      return
    }
    if (!val || !EMAIL_PATTERN.test(val)) return
    setEmailState('checking')
    setError('')
    try {
      const res = await api.get(`/auth/check-email?email=${encodeURIComponent(val)}`)
      if (res.data.exists) {
        setEmailState('existing')
        setTimeout(() => passwordRef.current?.focus(), 80)
      } else {
        setEmailState('new')
      }
    } catch {
      setEmailState('new')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (emailState === 'checking') return
    if (emailState === 'idle') {
      if (!EMAIL_PATTERN.test(email.trim()) && !isStudentNumber(email)) {
        setError(t.invalidIdentifier)
        return
      }
      await handleEmailBlur()
      return
    }
    if (!password || password.length < MIN_PASSWORD_LENGTH) {
      setError(PASSWORD_TOO_SHORT)
      return
    }
    setSubmitting(true)
    setError('')
    try {
      let res
      if (emailState === 'existing') {
        // The login endpoint is an OAuth2 password form, not JSON
        const params = new URLSearchParams()
        params.append('username', isStudentNumber(email) ? normalizeStudentNumber(email) : email.trim())
        params.append('password', password)
        res = await api.post('/auth/login', params, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        })
      } else {
        res = await api.post('/auth/register', {
          name, email: email.trim(), password, class_section: classSection, student_number: studentNumber,
        })
      }
      // Older backends can ignore newly required profile fields during signup.
      // Stop clearly instead of navigating to a profile endpoint they do not have.
      if (!Object.hasOwn(res.data, 'class_section') || !Object.hasOwn(res.data, 'student_number')) {
        if (emailState === 'new') setEmailState('existing')
        setError(t.profileServiceUnavailable)
        return
      }
      login(res.data.access_token, {
        id: res.data.student_id, name: res.data.name,
        is_teacher: !!res.data.is_teacher, class_section: res.data.class_section ?? null,
        role: res.data.role, is_admin: !!res.data.is_admin,
        student_number: res.data.student_number ?? null,
      })
      navigate(res.data.is_admin ? '/admin' : res.data.is_teacher ? '/teacher'
        : !res.data.class_section || !res.data.student_number ? '/complete-profile' : '/lessons')
    } catch (err) {
      const d = err.response?.data?.detail
      setError(typeof d === 'string' ? d : LOGIN_FAILED)
    } finally {
      setSubmitting(false)
    }
  }

  const resetEmail = () => {
    setEmailState('idle')
    setPassword('')
    setError('')
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', direction: lang === 'ar' ? 'rtl' : 'ltr', fontFamily: "var(--aq-font-arabic)" }}>

      <HeroPanel />

      {/* ═══ FORM PANEL ═══ */}
      <div style={{
        flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        padding: '40px 24px', background: 'var(--aq-ivory)',
      }}>
        <div style={{ width: '100%', maxWidth: 420 }}>

          {/* Back + Language Switch */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 }}>
            <Link to="/landing" style={{
              fontSize: 13, color: 'var(--aq-text-muted)', textDecoration: 'none',
              fontFamily: lang === 'ar' ? "var(--aq-font-arabic)" : "var(--aq-font-sans)",
              transition: 'color .2s',
            }}
              onMouseEnter={e => e.currentTarget.style.color = 'var(--aq-navy)'}
              onMouseLeave={e => e.currentTarget.style.color = 'var(--aq-text-muted)'}
            >{t.back}</Link>
            <LanguageSwitch lang={lang} onChange={setLang} />
          </div>

          {/* Mobile logo */}
          <div className="aq-mobile-logo" style={{ textAlign: 'center', marginBottom: 32 }}>
            <BrandMark size={60} style={{ margin: '0 auto 12px', display: 'block' }} />
            <h1 style={{ fontSize: 24, fontWeight: 700, color: 'var(--aq-navy)', fontFamily: "var(--aq-font-display)" }}>
              Arabiq Akademi
            </h1>
            <p style={{ fontSize: 13, color: 'var(--aq-text-muted)', marginTop: 4 }}>
              منصة تعلم اللغة العربية لطلاب كلية الإلهيات
            </p>
          </div>

          {/* Card */}
          <div style={{
            background: 'var(--aq-card)', borderRadius: 24, padding: '40px 36px',
            boxShadow: '0 4px 24px rgba(0,0,0,0.06)', border: '1px solid var(--aq-border)',
          }}>
            <CardHeading emailState={emailState} t={t} />

            <form onSubmit={handleSubmit}>

              {/* Email */}
              <div style={{ marginBottom: 18 }}>
                <label htmlFor="login-identifier" style={labelStyle}>{emailState === 'new' ? t.email : t.loginIdentifier}</label>
                <div style={{ position: 'relative' }}>
                  <span style={{ ...fieldIcon, color: 'var(--aq-text-muted)', fontSize: 16, pointerEvents: 'none' }}>✉</span>
                  <input id="login-identifier" type="text" value={email} autoComplete="username"
                    onChange={e => { setEmail(e.target.value); if (emailState !== 'idle') resetEmail() }}
                    onBlur={handleEmailBlur} required placeholder={t.identifierPlaceholder} dir="ltr"
                    style={{
                      ...inputStyle, paddingLeft: 42,
                      borderColor: emailState === 'existing' ? '#86EFAC' : emailState === 'new' ? '#93C5FD' : 'var(--aq-border)',
                    }}
                    onFocus={highlight}
                  />
                  {emailState === 'checking' && (
                    <span style={{ position: 'absolute', left: 14, top: '50%', width: 16, height: 16, border: '2px solid #C9A84C', borderTopColor: 'transparent', borderRadius: '50%', animation: 'aq-spin .7s linear infinite', display: 'inline-block' }} />
                  )}
                  {emailState === 'existing' && <span style={{ ...fieldIcon, color: '#22C55E', fontSize: 18, fontWeight: 700 }}>✓</span>}
                  {emailState === 'new' && <span style={{ ...fieldIcon, color: '#3B82F6', fontSize: 18, fontWeight: 700 }}>+</span>}
                </div>
              </div>

              {/* Name (new) */}
              {emailState === 'new' && (
                <div style={{ marginBottom: 18, animation: 'aq-fade-in .3s ease-out' }}>
                  <label style={labelStyle}>{t.name}</label>
                  <input value={name} onChange={e => setName(e.target.value)} required placeholder="أدخل اسمك الكامل"
                    style={inputStyle} onFocus={highlight} onBlur={unhighlight} />
                </div>
              )}

              {/* Password */}
              {(emailState === 'existing' || emailState === 'new') && (
                <div style={{ marginBottom: 18, animation: 'aq-fade-in .3s ease-out' }}>
                  <label style={labelStyle}>{t.password}</label>
                  <div style={{ position: 'relative' }}>
                    <span style={{ ...fieldIcon, color: 'var(--aq-text-muted)', fontSize: 16, pointerEvents: 'none' }}>🔒</span>
                    <input ref={passwordRef} type={showPwd ? 'text' : 'password'} value={password}
                      onChange={e => setPassword(e.target.value)} required placeholder="6 أحرف على الأقل" dir="ltr"
                      style={{ ...inputStyle, paddingLeft: 42, paddingRight: 42 }}
                      onFocus={highlight} onBlur={unhighlight} />
                    <button type="button" onClick={() => setShowPwd(v => !v)}
                      style={{ position: 'absolute', right: 14, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: 'var(--aq-text-muted)', fontSize: 14 }}>
                      {showPwd ? '🙈' : '👁'}
                    </button>
                  </div>
                </div>
              )}

              {/* Preparatory class section (new) */}
              {emailState === 'new' && (
                <>
                  <StudentNumberField value={studentNumber}
                    onChange={value => { setStudentNumber(value); setError('') }} t={t} />
                  <ClassSectionField value={classSection} onChange={setClassSection} t={t} />
                </>
              )}

              {/* Error */}
              {(error || sessionExpired) && (
                <div role="alert" style={{ background: '#FEF2F2', border: '1px solid #FECACA', color: '#DC2626', borderRadius: 14, padding: '12px 16px', fontSize: 13, marginBottom: 12, fontWeight: 500 }}>
                  {error || t.sessionExpired}
                </div>
              )}

              {/* Submit — "continue" until the email is checked, then login / sign-up */}
              <button type="submit" disabled={busy}
                style={{
                  width: '100%', padding: '14px', borderRadius: 14, border: 'none', cursor: 'pointer',
                  background: 'var(--aq-gradient-royal)', boxShadow: 'var(--aq-shadow-elegant)',
                  color: '#FAF8F3', fontSize: 16, fontWeight: 700, fontFamily: "var(--aq-font-arabic)",
                  transition: 'all .2s', opacity: busy ? 0.6 : 1, marginTop: 4, position: 'relative', overflow: 'hidden',
                }}
                onMouseEnter={e => { if (!submitting) e.target.style.transform = 'translateY(-1px)' }}
                onMouseLeave={e => e.target.style.transform = 'none'}>
                {busy ? (
                  <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}>
                    <span style={{ width: 18, height: 18, border: '2px solid rgba(255,255,255,0.3)', borderTopColor: '#fff', borderRadius: '50%', animation: 'aq-spin .7s linear infinite', display: 'inline-block' }} />
                    {submitting ? t.loading : t.checking}
                  </span>
                ) : emailState === 'existing' ? t.login + ' ←'
                  : emailState === 'new' ? t.signup + ' ←'
                  : t.next + ' ←'}
                <span style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: 2, background: 'var(--aq-gradient-gold)' }} />
              </button>

              {emailState === 'idle' && (
                <p style={{ textAlign: 'center', fontSize: 12, color: 'var(--aq-text-muted)', marginTop: 12 }}>
                  {t.hint}
                </p>
              )}
            </form>

            {/* Divider + Guest */}
            <div style={{ position: 'relative', marginTop: 24, paddingTop: 20 }}>
              <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 1, background: 'var(--aq-border)' }} />
              <div style={{ position: 'absolute', top: -8, left: '50%', transform: 'translateX(-50%)', background: 'var(--aq-card)', padding: '0 16px', fontSize: 12, color: 'var(--aq-text-muted)' }}>أو</div>
              <Link to="/lessons" style={{
                display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
                width: '100%', padding: '14px', borderRadius: 14, textDecoration: 'none',
                border: '2px solid rgba(201,168,76,0.4)', background: 'transparent',
                color: 'var(--aq-navy)', fontSize: 15, fontWeight: 600, fontFamily: "var(--aq-font-arabic)",
                transition: 'all .2s',
              }}
                onMouseEnter={e => { e.currentTarget.style.borderColor = '#C9A84C'; e.currentTarget.style.background = 'rgba(201,168,76,0.05)' }}
                onMouseLeave={e => { e.currentTarget.style.borderColor = 'rgba(201,168,76,0.4)'; e.currentTarget.style.background = 'transparent' }}>
                {t.guest}
              </Link>
            </div>
          </div>

          {/* Footer */}
          <div style={{ textAlign: 'center', marginTop: 24 }}>
            <div style={{ width: 48, height: 1, background: 'var(--aq-border)', margin: '0 auto 8px' }} />
            <p style={{ fontSize: 12, color: 'var(--aq-text-muted)' }}>{t.footer}</p>
            <p style={{ fontSize: 10, letterSpacing: '0.2em', color: 'rgba(107,122,141,0.6)', marginTop: 4 }}>KARABÜK ÜNİVERSİTESİ</p>
          </div>
        </div>
      </div>

      <style>{`
        @media (max-width: 1023px) { .aq-hero-panel { display: none !important; } }
        @media (min-width: 1024px) { .aq-mobile-logo { display: none !important; } }
      `}</style>
    </div>
  )
}
