import logo from '../../assets/logo.png'
import { ArabesqueCorner, NeuralBackdrop } from './decorations'

const STATS = [
  { icon: '\u{1F4D6}', v: '48', l: 'وحدة دراسية' },
  { icon: '✍️', v: '+4000', l: 'تمرين تفاعلي' },
  { icon: '\u{1F9E0}', v: 'AI', l: 'محادثة ذكية' },
]

/** The navy half of the login page. Hidden below 1024px (see LoginPage). */
export default function HeroPanel() {
  return (
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
        {STATS.map(s => (
          <div key={s.l} style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <span style={{ fontSize: 18 }}>{s.icon}</span>
            <div style={{ fontSize: 24, fontWeight: 600, color: '#D4B96A', fontFamily: "var(--aq-font-display)" }}>{s.v}</div>
            <div style={{ fontSize: 12, color: 'rgba(250,248,243,0.6)', fontFamily: "var(--aq-font-arabic)" }}>{s.l}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
