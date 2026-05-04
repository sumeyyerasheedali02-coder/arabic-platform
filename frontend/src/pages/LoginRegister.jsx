import { useState, useRef } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../api/client'

// email check states: 'idle' | 'checking' | 'existing' | 'new'

export default function LoginRegister() {
  const [email, setEmail]         = useState('')
  const [emailState, setEmailState] = useState('idle')   // idle | checking | existing | new
  const [existingName, setExistingName] = useState('')
  const [name, setName]           = useState('')
  const [password, setPassword]   = useState('')
  const [year, setYear]           = useState(1)
  const [error, setError]         = useState('')
  const [submitting, setSubmitting] = useState(false)
  const passwordRef               = useRef(null)
  const { login }                 = useAuth()
  const navigate                  = useNavigate()

  const inputCls = {
    width: '100%', padding: '11px 16px', borderRadius: 12,
    background: '#1e2231', border: '1px solid #2a3045',
    color: '#fff', fontSize: 14, outline: 'none',
    transition: 'border-color .15s',
    fontFamily: 'DM Sans, sans-serif',
  }

  const handleEmailBlur = async () => {
    const val = email.trim()
    if (!val || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) return
    setEmailState('checking')
    setError('')
    try {
      const res = await api.get(`/auth/check-email?email=${encodeURIComponent(val)}`)
      if (res.data.exists) {
        setExistingName(res.data.name)
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
    setSubmitting(true)
    setError('')
    try {
      let res
      if (emailState === 'existing') {
        const params = new URLSearchParams()
        params.append('username', email.trim())
        params.append('password', password)
        res = await api.post('/auth/login', params, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        })
      } else {
        res = await api.post('/auth/register', {
          name, email: email.trim(), password, year: Number(year),
        })
      }
      login(res.data.access_token, { id: res.data.student_id, name: res.data.name })
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'حدث خطأ، حاول مجدداً')
    } finally {
      setSubmitting(false)
    }
  }

  const resetEmail = () => {
    setEmailState('idle')
    setExistingName('')
    setPassword('')
    setError('')
  }

  return (
    <div className="min-h-screen flex" dir="rtl">

      {/* ── Decorative left panel ── */}
      <div className="hidden lg:flex flex-1 bg-gradient-to-br from-primary-900 via-primary-800 to-primary-700 items-center justify-center p-12 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="absolute rounded-full border border-white"
              style={{ width: `${140 + i * 90}px`, height: `${140 + i * 90}px`, top: `${8 + i * 7}%`, right: `${4 + i * 5}%` }} />
          ))}
        </div>
        <div className="relative text-center text-white">
          <div className="text-7xl mb-6">📚</div>
          <h1 className="text-4xl font-bold mb-4 leading-snug">العربية بين يديك</h1>
          <p className="text-primary-200 text-lg max-w-xs mx-auto leading-relaxed">
            منصة تعليمية متكاملة لتعلم اللغة العربية لطلاب كلية الإلهيات
          </p>
          <div className="mt-10 grid grid-cols-3 gap-4 text-center">
            {[['📖','دروس تفاعلية'],['🤖','مساعد ذكي'],['🗂️','بطاقات SRS']].map(([icon, label]) => (
              <div key={label} className="bg-white/10 rounded-2xl p-4 backdrop-blur-sm border border-white/10">
                <div className="text-2xl mb-2">{icon}</div>
                <div className="text-sm text-primary-200">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── Form panel ── */}
      <div className="flex-1 flex items-center justify-center p-6 bg-dark-base">
        <div className="w-full max-w-md">

          <div className="lg:hidden text-center mb-8">
            <span className="text-5xl">📚</span>
            <h1 className="text-2xl font-bold text-white mt-3">العربية بين يديك</h1>
          </div>

          <div className="bg-dark-surface rounded-3xl border border-dark-border p-8 shadow-2xl animate-fade-in">

            {/* ── Greeting for existing user ── */}
            {emailState === 'existing' && (
              <div style={{ marginBottom: 24, textAlign: 'center' }}>
                <div style={{ fontSize: 28, marginBottom: 4 }}>👋</div>
                <div style={{ fontSize: 20, fontWeight: 700, color: '#fff', marginBottom: 4 }}>
                  مرحباً {existingName}!
                </div>
                <div style={{ fontSize: 12, color: '#64748b' }}>أدخل كلمة المرور للدخول</div>
              </div>
            )}

            {/* ── Header for new user ── */}
            {emailState === 'new' && (
              <div style={{ marginBottom: 24, textAlign: 'center' }}>
                <div style={{ fontSize: 20, fontWeight: 700, color: '#fff', marginBottom: 4 }}>
                  حساب جديد
                </div>
                <div style={{ fontSize: 12, color: '#64748b' }}>أكمل بياناتك لإنشاء حسابك</div>
              </div>
            )}

            {/* ── Default header ─�� */}
            {(emailState === 'idle' || emailState === 'checking') && (
              <h2 className="text-2xl font-bold text-white mb-6 text-center">
                {emailState === 'checking' ? '...' : 'أدخل بريدك الإلكتروني'}
              </h2>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">

              {/* ── Email field ── */}
              <div>
                <label style={{ display: 'block', fontSize: 13, fontWeight: 500, color: '#94a3b8', marginBottom: 6 }}>
                  البريد الإلكتروني
                </label>
                <div style={{ position: 'relative' }}>
                  <input
                    type="email"
                    value={email}
                    onChange={e => { setEmail(e.target.value); if (emailState !== 'idle') resetEmail() }}
                    onBlur={handleEmailBlur}
                    required
                    placeholder="example@university.edu"
                    dir="ltr"
                    style={{
                      ...inputCls,
                      borderColor: emailState === 'existing' ? '#22c55e44'
                                 : emailState === 'new'      ? '#3b82f644'
                                 : '#2a3045',
                      paddingLeft: emailState !== 'idle' ? 36 : 16,
                    }}
                    onFocus={e => e.target.style.borderColor = '#4f6ef7'}
                  />
                  {/* status dot */}
                  {emailState === 'checking' && (
                    <span style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', width: 14, height: 14, border: '2px solid #4f6ef7', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin .7s linear infinite', display: 'inline-block' }} />
                  )}
                  {emailState === 'existing' && (
                    <span style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: '#22c55e', fontSize: 15 }}>✓</span>
                  )}
                  {emailState === 'new' && (
                    <span style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: '#3b82f6', fontSize: 15 }}>+</span>
                  )}
                </div>
              </div>

              {/* ── Name field (new users only) ── */}
              {emailState === 'new' && (
                <div className="animate-fade-in">
                  <label style={{ display: 'block', fontSize: 13, fontWeight: 500, color: '#94a3b8', marginBottom: 6 }}>
                    الاسم الكامل
                  </label>
                  <input
                    value={name}
                    onChange={e => setName(e.target.value)}
                    required
                    placeholder="أدخل اسمك الكامل"
                    style={inputCls}
                    onFocus={e => e.target.style.borderColor = '#4f6ef7'}
                    onBlur={e => e.target.style.borderColor = '#2a3045'}
                  />
                </div>
              )}

              {/* ── Password field (existing or new) ── */}
              {(emailState === 'existing' || emailState === 'new') && (
                <div className="animate-fade-in">
                  <label style={{ display: 'block', fontSize: 13, fontWeight: 500, color: '#94a3b8', marginBottom: 6 }}>
                    كلمة المرور
                  </label>
                  <input
                    ref={passwordRef}
                    type="password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    required
                    placeholder="••••••••"
                    style={inputCls}
                    onFocus={e => e.target.style.borderColor = '#4f6ef7'}
                    onBlur={e => e.target.style.borderColor = '#2a3045'}
                  />
                </div>
              )}

              {/* ── Year (new users only) ── */}
              {emailState === 'new' && (
                <div className="animate-fade-in">
                  <label style={{ display: 'block', fontSize: 13, fontWeight: 500, color: '#94a3b8', marginBottom: 6 }}>
                    السنة الدراسية
                  </label>
                  <select
                    value={year}
                    onChange={e => setYear(e.target.value)}
                    style={{ ...inputCls, cursor: 'pointer' }}
                  >
                    {[1,2,3,4].map(y => <option key={y} value={y}>السنة {y}</option>)}
                  </select>
                </div>
              )}

              {/* ── Error ── */}
              {error && (
                <div style={{ background: 'rgba(239,68,68,.1)', border: '1px solid rgba(239,68,68,.3)', color: '#f87171', borderRadius: 12, padding: '10px 14px', fontSize: 13 }}>
                  {error}
                </div>
              )}

              {/* ── Submit button ── */}
              {(emailState === 'existing' || emailState === 'new') && (
                <button
                  type="submit"
                  disabled={submitting}
                  className="w-full py-3 bg-primary-600 hover:bg-primary-700 disabled:bg-primary-600/40 text-white font-bold rounded-xl transition-all duration-200 animate-fade-in"
                  style={{ marginTop: 4 }}
                >
                  {submitting ? (
                    <span className="flex items-center justify-center gap-2">
                      <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      جاري التحميل...
                    </span>
                  ) : emailState === 'existing' ? 'دخول' : 'إنشاء الحساب'}
                </button>
              )}

              {/* ── First step: just the "Continue" hint ── */}
              {emailState === 'idle' && (
                <p style={{ textAlign: 'center', fontSize: 12, color: '#475569', marginTop: 4 }}>
                  سيتم التحقق تلقائياً عند المغادرة
                </p>
              )}

            </form>

            {/* ── Guest access ── */}
            <div style={{ marginTop: 20, textAlign: 'center', borderTop: '1px solid rgba(255,255,255,.07)', paddingTop: 16 }}>
              <span style={{ fontSize: 12, color: '#475569' }}>أو </span>
              <Link to="/lessons" style={{ fontSize: 12, color: '#64748b', textDecoration: 'underline', textDecorationColor: 'rgba(100,116,139,.4)' }}>
                تصفح كضيف بدون تسجيل
              </Link>
            </div>

          </div>
        </div>
      </div>
    </div>
  )
}
