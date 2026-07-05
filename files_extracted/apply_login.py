import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PATH = r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages\LoginRegister.jsx"

CODE = r"""import { useState, useRef } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../api/client'
import logo from '../assets/logo.png'

export default function LoginRegister() {
  const [email, setEmail]         = useState('')
  const [emailState, setEmailState] = useState('idle')
  const [existingName, setExistingName] = useState('')
  const [name, setName]           = useState('')
  const [password, setPassword]   = useState('')
  const [showPwd, setShowPwd]     = useState(false)
  const [year, setYear]           = useState(1)
  const [error, setError]         = useState('')
  const [submitting, setSubmitting] = useState(false)
  const passwordRef               = useRef(null)
  const { login }                 = useAuth()
  const navigate                  = useNavigate()

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
    if (emailState === 'idle' || emailState === 'checking') {
      await handleEmailBlur()
      return
    }
    if (!password || password.length < 6) {
      setError('\u0623\u062f\u062e\u0644 \u0643\u0644\u0645\u0629 \u0645\u0631\u0648\u0631 \u0645\u0646 6 \u0623\u062d\u0631\u0641 \u0639\u0644\u0649 \u0627\u0644\u0623\u0642\u0644')
      return
    }
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
      const d = err.response?.data?.detail
      setError(typeof d === 'string' ? d : '\u062a\u0623\u0643\u062f \u0645\u0646 \u0627\u0644\u0628\u0631\u064a\u062f \u0648\u0643\u0644\u0645\u0629 \u0627\u0644\u0645\u0631\u0648\u0631 (6 \u0623\u062d\u0631\u0641 \u0639\u0644\u0649 \u0627\u0644\u0623\u0642\u0644)')
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

  /* ═══ Inline Styles ═══ */
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

  return (
    <div style={{ minHeight: '100vh', display: 'flex', direction: 'rtl', fontFamily: "var(--aq-font-arabic)" }}>

      {/* ═══ HERO PANEL ═══ */}
      <div style={{
        flex: 1, background: 'var(--aq-gradient-hero)', position: 'relative', overflow: 'hidden',
        display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: '48px',
      }} className="aq-hero-panel">
        <NeuralBackdrop />
        <ArabesqueCorner />

        {/* Logo + Title */}
        <div style={{ position: 'relative', zIndex: 10, display: 'flex', alignItems: 'center', gap: 16 }}>
          <img src={logo} alt="Arabiq Akademi" width={64} height={64}
            style={{ width: 64, height: 64, filter: 'drop-shadow(0 4px 20px rgba(201,168,76,0.35))' }} />
          <div>
            <h1 style={{ fontSize: 28, fontWeight: 600, color: '#FAF8F3', fontFamily: "var(--aq-font-display)", letterSpacing: '-0.01em' }}>
              Arabiq Akademi
            </h1>
            <p style={{ fontSize: 14, color: 'rgba(212,185,106,0.9)', marginTop: 4, fontFamily: "var(--aq-font-arabic)" }}>
              تعليم اللغة العربية بذكاء
            </p>
          </div>
        </div>

        {/* Welcome text */}
        <div style={{ position: 'relative', zIndex: 10, maxWidth: 420 }}>
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: 8, borderRadius: 999,
            border: '1px solid rgba(201,168,76,0.3)', background: 'rgba(201,168,76,0.1)',
            padding: '6px 16px', fontSize: 12, fontWeight: 500, color: '#D4B96A', backdropFilter: 'blur(4px)',
          }}>
            ✦ مدعوم بالذكاء الاصطناعي
          </div>
          <h2 style={{
            fontSize: 38, fontWeight: 500, lineHeight: 1.3, color: '#FAF8F3', marginTop: 20,
            fontFamily: "var(--aq-font-arabic)",
          }}>
            أهلاً بك في رحلة<br />
            <span style={{ color: '#C9A84C' }}>إتقان العربية</span>
          </h2>
          <p style={{ fontSize: 15, lineHeight: 1.8, color: 'rgba(250,248,243,0.7)', marginTop: 12, fontFamily: "var(--aq-font-sans)" }}>
            Arapça ustalık yolculuğuna hoş geldin. İlahiyat öğrencileri için tasarlanmış yapay zekâ destekli platform.
          </p>
        </div>

        {/* Stats */}
        <div style={{
          position: 'relative', zIndex: 10, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)',
          gap: 16, borderTop: '1px solid rgba(201,168,76,0.2)', paddingTop: 28,
        }}>
          {[
            { icon: '\u{1F4D6}', v: '48', l: 'وحدة دراسية' },
            { icon: '\u270D\uFE0F', v: '+4000', l: 'تمرين تفاعلي' },
            { icon: '\u{1F9E0}', v: 'AI', l: 'محادثة ذكية' },
          ].map(s => (
            <div key={s.l} style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              <span style={{ fontSize: 18 }}>{s.icon}</span>
              <div style={{ fontSize: 24, fontWeight: 600, color: '#D4B96A', fontFamily: "var(--aq-font-display)" }}>{s.v}</div>
              <div style={{ fontSize: 12, color: 'rgba(250,248,243,0.6)', fontFamily: "var(--aq-font-arabic)" }}>{s.l}</div>
            </div>
          ))}
        </div>
      </div>

      {/* ═══ FORM PANEL ═══ */}
      <div style={{
        flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        padding: '40px 24px', background: 'var(--aq-ivory)',
      }}>
        <div style={{ width: '100%', maxWidth: 420 }}>

          {/* Mobile logo */}
          <div className="aq-mobile-logo" style={{ textAlign: 'center', marginBottom: 32 }}>
            <img src={logo} alt="Arabiq Akademi" width={60} height={60}
              style={{ width: 60, height: 60, margin: '0 auto 12px', display: 'block' }} />
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

            {/* Header by state */}
            {emailState === 'existing' && (
              <div style={{ textAlign: 'center', marginBottom: 28, animation: 'aq-fade-in .3s ease-out' }}>
                <div style={{
                  width: 56, height: 56, borderRadius: 16, background: '#F0FDF4',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: 28, margin: '0 auto 12px', border: '1px solid #BBF7D0',
                }}>👋</div>
                <h2 style={{ fontSize: 22, fontWeight: 800, color: 'var(--aq-navy)' }}>مرحباً {existingName}!</h2>
                <p style={{ fontSize: 13, color: 'var(--aq-text-muted)', marginTop: 4 }}>أدخل كلمة المرور للمتابعة</p>
              </div>
            )}
            {emailState === 'new' && (
              <div style={{ textAlign: 'center', marginBottom: 28, animation: 'aq-fade-in .3s ease-out' }}>
                <div style={{
                  width: 56, height: 56, borderRadius: 16, background: '#EFF6FF',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: 28, margin: '0 auto 12px', border: '1px solid #BFDBFE',
                }}>🎓</div>
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, fontSize: 12, fontWeight: 600, letterSpacing: '0.15em', color: '#C9A84C', marginBottom: 8 }}>
                  <span style={{ width: 32, height: 1, background: '#C9A84C', display: 'inline-block' }} />أكاديمي
                </div>
                <h2 style={{ fontSize: 22, fontWeight: 800, color: 'var(--aq-navy)' }}>حساب جديد</h2>
                <p style={{ fontSize: 13, color: 'var(--aq-text-muted)', marginTop: 4 }}>أكمل بياناتك لبدء رحلة التعلّم</p>
              </div>
            )}
            {(emailState === 'idle' || emailState === 'checking') && (
              <div style={{ textAlign: 'center', marginBottom: 28 }}>
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, fontSize: 12, fontWeight: 600, letterSpacing: '0.15em', color: '#C9A84C', marginBottom: 8 }}>
                  <span style={{ width: 32, height: 1, background: '#C9A84C', display: 'inline-block' }} />أكاديمي
                </div>
                <h2 style={{ fontSize: 28, fontWeight: 700, color: 'var(--aq-navy)' }}>
                  {emailState === 'checking' ? 'جارٍ التحقق...' : 'تسجيل الدخول'}
                </h2>
                <p style={{ fontSize: 13, color: 'var(--aq-text-muted)', marginTop: 6 }}>أدخل بريدك الإلكتروني للبدء</p>
              </div>
            )}

            <form onSubmit={handleSubmit}>

              {/* Email */}
              <div style={{ marginBottom: 18 }}>
                <label style={labelStyle}>البريد الإلكتروني</label>
                <div style={{ position: 'relative' }}>
                  <span style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: 'var(--aq-text-muted)', fontSize: 16, pointerEvents: 'none' }}>✉</span>
                  <input type="email" value={email}
                    onChange={e => { setEmail(e.target.value); if (emailState !== 'idle') resetEmail() }}
                    onBlur={handleEmailBlur} required placeholder="name@karabuk.edu.tr" dir="ltr"
                    style={{
                      ...inputStyle, paddingLeft: 42,
                      borderColor: emailState === 'existing' ? '#86EFAC' : emailState === 'new' ? '#93C5FD' : 'var(--aq-border)',
                    }}
                    onFocus={e => { e.target.style.borderColor = '#C9A84C'; e.target.style.boxShadow = '0 0 0 3px rgba(201,168,76,0.12)' }}
                  />
                  {emailState === 'checking' && (
                    <span style={{ position: 'absolute', left: 14, top: '50%', width: 16, height: 16, border: '2px solid #C9A84C', borderTopColor: 'transparent', borderRadius: '50%', animation: 'aq-spin .7s linear infinite', display: 'inline-block' }} />
                  )}
                  {emailState === 'existing' && <span style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: '#22C55E', fontSize: 18, fontWeight: 700 }}>✓</span>}
                  {emailState === 'new' && <span style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: '#3B82F6', fontSize: 18, fontWeight: 700 }}>+</span>}
                </div>
              </div>

              {/* Name (new) */}
              {emailState === 'new' && (
                <div style={{ marginBottom: 18, animation: 'aq-fade-in .3s ease-out' }}>
                  <label style={labelStyle}>الاسم الكامل</label>
                  <input value={name} onChange={e => setName(e.target.value)} required placeholder="أدخل اسمك الكامل"
                    style={inputStyle}
                    onFocus={e => { e.target.style.borderColor = '#C9A84C'; e.target.style.boxShadow = '0 0 0 3px rgba(201,168,76,0.12)' }}
                    onBlur={e => { e.target.style.borderColor = 'var(--aq-border)'; e.target.style.boxShadow = 'none' }} />
                </div>
              )}

              {/* Password */}
              {(emailState === 'existing' || emailState === 'new') && (
                <div style={{ marginBottom: 18, animation: 'aq-fade-in .3s ease-out' }}>
                  <label style={labelStyle}>كلمة المرور</label>
                  <div style={{ position: 'relative' }}>
                    <span style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: 'var(--aq-text-muted)', fontSize: 16, pointerEvents: 'none' }}>🔒</span>
                    <input ref={passwordRef} type={showPwd ? 'text' : 'password'} value={password}
                      onChange={e => setPassword(e.target.value)} required placeholder="6 أحرف على الأقل" dir="ltr"
                      style={{ ...inputStyle, paddingLeft: 42, paddingRight: 42 }}
                      onFocus={e => { e.target.style.borderColor = '#C9A84C'; e.target.style.boxShadow = '0 0 0 3px rgba(201,168,76,0.12)' }}
                      onBlur={e => { e.target.style.borderColor = 'var(--aq-border)'; e.target.style.boxShadow = 'none' }} />
                    <button type="button" onClick={() => setShowPwd(v => !v)}
                      style={{ position: 'absolute', right: 14, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: 'var(--aq-text-muted)', fontSize: 14 }}>
                      {showPwd ? '🙈' : '👁'}
                    </button>
                  </div>
                </div>
              )}

              {/* Year (new) */}
              {emailState === 'new' && (
                <div style={{ marginBottom: 18, animation: 'aq-fade-in .3s ease-out' }}>
                  <label style={labelStyle}>السنة الدراسية</label>
                  <select value={year} onChange={e => setYear(e.target.value)}
                    style={{ ...inputStyle, cursor: 'pointer', appearance: 'auto' }}>
                    {[1,2,3,4].map(y => <option key={y} value={y}>السنة {y}</option>)}
                  </select>
                </div>
              )}

              {/* Error */}
              {error && (
                <div style={{ background: '#FEF2F2', border: '1px solid #FECACA', color: '#DC2626', borderRadius: 14, padding: '12px 16px', fontSize: 13, marginBottom: 12, fontWeight: 500 }}>
                  {error}
                </div>
              )}

              {/* Submit */}
              {(emailState === 'existing' || emailState === 'new') && (
                <button type="submit" disabled={submitting}
                  style={{
                    width: '100%', padding: '14px', borderRadius: 14, border: 'none', cursor: 'pointer',
                    background: 'var(--aq-gradient-royal)', boxShadow: 'var(--aq-shadow-elegant)',
                    color: '#FAF8F3', fontSize: 16, fontWeight: 700, fontFamily: "var(--aq-font-arabic)",
                    transition: 'all .2s', opacity: submitting ? 0.6 : 1, marginTop: 4, position: 'relative', overflow: 'hidden',
                  }}
                  onMouseEnter={e => { if (!submitting) e.target.style.transform = 'translateY(-1px)' }}
                  onMouseLeave={e => e.target.style.transform = 'none'}>
                  {submitting ? (
                    <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}>
                      <span style={{ width: 18, height: 18, border: '2px solid rgba(255,255,255,0.3)', borderTopColor: '#fff', borderRadius: '50%', animation: 'aq-spin .7s linear infinite', display: 'inline-block' }} />
                      جارٍ التحميل...
                    </span>
                  ) : emailState === 'existing' ? 'تسجيل الدخول ←' : 'إنشاء الحساب ←'}
                  <span style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: 2, background: 'var(--aq-gradient-gold)' }} />
                </button>
              )}

              {emailState === 'idle' && (
                <p style={{ textAlign: 'center', fontSize: 12, color: 'var(--aq-text-muted)', marginTop: 12 }}>
                  أدخل بريدك واضغط Tab أو Enter للمتابعة
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
                تصفّح كضيف بدون تسجيل
              </Link>
            </div>
          </div>

          {/* Footer */}
          <div style={{ textAlign: 'center', marginTop: 24 }}>
            <div style={{ width: 48, height: 1, background: 'var(--aq-border)', margin: '0 auto 8px' }} />
            <p style={{ fontSize: 12, color: 'var(--aq-text-muted)' }}>جامعة كارابوك — كلية الإلهيات</p>
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

/* ═══ Decorative: Neural Network Backdrop ═══ */
function NeuralBackdrop() {
  const nodes = [
    {cx:10,cy:20},{cx:25,cy:12},{cx:42,cy:25},{cx:18,cy:45},{cx:35,cy:55},
    {cx:8,cy:70},{cx:28,cy:82},{cx:48,cy:72},{cx:55,cy:40},{cx:70,cy:18},
    {cx:82,cy:35},{cx:90,cy:60},{cx:75,cy:78},{cx:60,cy:90},
  ]
  const links = [[0,1],[1,2],[2,8],[0,3],[3,4],[3,5],[5,6],[4,6],[4,7],[7,8],[8,9],[9,10],[10,11],[11,12],[12,13],[7,13],[2,9],[8,11]]
  return (
    <svg style={{ position:'absolute',inset:0,width:'100%',height:'100%',opacity:0.4,pointerEvents:'none' }} viewBox="0 0 100 100" preserveAspectRatio="none">
      {links.map(([a,b],i) => (
        <line key={i} x1={nodes[a].cx} y1={nodes[a].cy} x2={nodes[b].cx} y2={nodes[b].cy}
          stroke="#C9A84C" strokeWidth="0.08" opacity="0.5" />
      ))}
      {nodes.map((n,i) => (
        <circle key={i} cx={n.cx} cy={n.cy} r={i%3===0?0.5:0.3} fill="#D4B96A"
          style={{ animation:`aq-pulse-node 3s ease-in-out infinite`, animationDelay:`${(i%5)*0.4}s`, transformOrigin:`${n.cx}px ${n.cy}px` }} />
      ))}
    </svg>
  )
}

/* ═══ Decorative: Arabesque Corner ═══ */
function ArabesqueCorner() {
  return (
    <svg style={{ position:'absolute',bottom:-80,left:-80,width:384,height:384,color:'#C9A84C',opacity:0.08,pointerEvents:'none' }}
      viewBox="0 0 200 200" fill="none">
      <g stroke="currentColor" strokeWidth="0.8">
        <circle cx="100" cy="100" r="90" />
        <circle cx="100" cy="100" r="70" />
        <circle cx="100" cy="100" r="50" />
        {Array.from({length:16}).map((_,i) => {
          const a = (i*Math.PI*2)/16
          return <line key={i} x1={100+Math.cos(a)*50} y1={100+Math.sin(a)*50} x2={100+Math.cos(a)*90} y2={100+Math.sin(a)*90} />
        })}
        {Array.from({length:8}).map((_,i) => {
          const a = (i*Math.PI*2)/8+Math.PI/8
          return <polygon key={i} points={`${100+Math.cos(a)*70},${100+Math.sin(a)*70} ${100+Math.cos(a+0.2)*90},${100+Math.sin(a+0.2)*90} ${100+Math.cos(a-0.2)*90},${100+Math.sin(a-0.2)*90}`} />
        })}
      </g>
    </svg>
  )
}
"""

open(PATH, "w", encoding="utf-8").write(CODE)
print("\u2705 \u062a\u0645 \u062a\u0637\u0628\u064a\u0642 \u0627\u0644\u062a\u0635\u0645\u064a\u0645 \u0627\u0644\u062c\u062f\u064a\u062f \u0644\u0635\u0641\u062d\u0629 \u0627\u0644\u062f\u062e\u0648\u0644")