import { Link } from 'react-router-dom'

function Logo() {
  return (
    <svg width="140" height="140" viewBox="0 0 200 200" style={{ filter: 'drop-shadow(0 10px 40px rgba(201,168,76,0.45))' }}>
      <defs>
        <radialGradient id="goldGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#E8D48A" />
          <stop offset="100%" stopColor="#C9A84C" />
        </radialGradient>
      </defs>
      <circle cx="100" cy="100" r="78" fill="none" stroke="url(#goldGrad)" strokeWidth="1.5" strokeDasharray="3 4" opacity="0.85" />
      <circle cx="100" cy="100" r="68" fill="none" stroke="#C9A84C" strokeWidth="0.6" opacity="0.4" />
      {Array.from({ length: 12 }).map((_, i) => {
        const a = (i * Math.PI * 2) / 12
        const x = 100 + Math.cos(a) * 78
        const y = 100 + Math.sin(a) * 78
        return <circle key={i} cx={x} cy={y} r="2.2" fill="#E8D48A" />
      })}
      <text x="100" y="135" textAnchor="middle" fontFamily="'Amiri', serif" fontSize="110" fontWeight="700" fill="#0F2044">ع</text>
    </svg>
  )
}

export default function Landing() {
  const stats = [
    { v: '48',    l: 'وحدة دراسية' },
    { v: '+1000', l: 'مفردة (AR·TR·EN)' },
    { v: '+140',  l: 'حوار تفاعلي' },
    { v: '+4000', l: 'تمرين' },
    { v: 'AI',    l: 'محادثة ذكية' },
  ]

  return (
    <main dir="rtl" style={{
      minHeight: '100vh', display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      background: 'linear-gradient(135deg, #0B1426 0%, #0F2044 50%, #162952 100%)',
      position: 'relative', overflow: 'hidden', padding: '48px 24px',
      fontFamily: "'Cairo', 'Amiri', sans-serif",
    }}>
      <div aria-hidden style={{
        position: 'absolute', inset: 0, opacity: 0.4,
        background: 'radial-gradient(circle at 50% 30%, rgba(42,82,152,0.55), transparent 60%)',
        pointerEvents: 'none',
      }} />

      <div style={{ position: 'relative', zIndex: 10, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', maxWidth: 1100 }}>
        <div style={{ animation: 'aqFloat 6s ease-in-out infinite' }}>
          <Logo />
        </div>

        <div style={{
          marginTop: 32, display: 'inline-flex', alignItems: 'center', gap: 8,
          border: '1px solid rgba(201,168,76,0.4)', background: 'rgba(201,168,76,0.08)',
          color: '#E8D48A', padding: '8px 20px', borderRadius: 9999,
          fontSize: 13, fontWeight: 500, backdropFilter: 'blur(8px)',
        }}>
          <span aria-hidden style={{ color: '#E8D48A' }}>✦</span>
          مدعوم بالذكاء الاصطناعي
        </div>

        <h1 style={{
          marginTop: 28, fontFamily: "'Cormorant Garamond', 'Amiri', serif",
          fontSize: 'clamp(2.8rem, 6vw, 5rem)', fontWeight: 500,
          color: '#F9F7F2', lineHeight: 1.1, letterSpacing: '-0.02em',
        }}>
          Arabiq Akademi
        </h1>

        <p style={{ marginTop: 18, maxWidth: 640, fontSize: 18, lineHeight: 1.7, color: 'rgba(249,247,242,0.78)' }}>
          منصة تفاعلية لتعليم اللغة العربية
          <br />
          <span style={{ color: '#E8D48A' }}>لطلاب كلية الإلهيات ومتعلّمي اللغة العربية</span>
        </p>

        <p lang="tr" style={{ marginTop: 10, fontSize: 14, color: 'rgba(249,247,242,0.62)' }}>
          İlahiyat Fakültesi öğrencileri ve Arapça öğrenenler için
        </p>

        <p style={{ marginTop: 4, fontSize: 13, color: 'rgba(249,247,242,0.5)' }}>
          Karabük Üniversitesi İlahiyat Fakültesi
        </p>

        <Link to="/login" className="aq-cta" style={{
          marginTop: 40, display: 'inline-flex', alignItems: 'center', gap: 12,
          padding: '14px 36px',
          background: 'linear-gradient(135deg, #C9A84C 0%, #DCC06A 100%)',
          color: '#0F2044', fontSize: 16, fontWeight: 600,
          borderRadius: 9999, textDecoration: 'none',
          boxShadow: '0 10px 30px -10px rgba(201,168,76,0.5)',
          transition: 'transform 0.25s ease, box-shadow 0.25s ease',
        }}>
          ابدأ الآن
          <span aria-hidden style={{ fontSize: 18 }}>←</span>
        </Link>

        <div style={{
          marginTop: 64, display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(110px, 1fr))',
          gap: 28, width: '100%', maxWidth: 880, paddingTop: 32,
          borderTop: '1px solid rgba(201,168,76,0.2)',
        }}>
          {stats.map((s) => (
            <div key={s.l} style={{ textAlign: 'center' }}>
              <div style={{
                fontFamily: "'Cormorant Garamond', 'Amiri', serif",
                fontSize: 'clamp(1.8rem, 3vw, 2.4rem)', fontWeight: 600,
                color: '#C9A84C', lineHeight: 1,
              }}>
                {s.v}
              </div>
              <div style={{ marginTop: 8, fontSize: 12, color: 'rgba(249,247,242,0.6)' }}>
                {s.l}
              </div>
            </div>
          ))}
        </div>
      </div>

      <style>{`
        @keyframes aqFloat {
          0%, 100% { transform: translateY(0); }
          50%      { transform: translateY(-8px); }
        }
        .aq-cta:hover {
          transform: translateY(-2px) scale(1.02);
          box-shadow: 0 14px 36px -10px rgba(201,168,76,0.65);
        }
      `}</style>
    </main>
  )
}
