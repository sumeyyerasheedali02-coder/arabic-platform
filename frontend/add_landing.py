import sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = r"C:\Users\SD\Desktop\arabic_platform\frontend\src"

# ══════════════════════════════════════════════════════════
# 1. إنشاء Landing.jsx
# ══════════════════════════════════════════════════════════
LANDING = r"""import { Link } from 'react-router-dom'
import logo from '../assets/logo.png'

export default function Landing() {
  const stats = [
    { v: '48', l: '\u0648\u062d\u062f\u0629 \u062f\u0631\u0627\u0633\u064a\u0629' },
    { v: '+1000', l: '\u0645\u0641\u0631\u062f\u0629 (AR\u00b7TR\u00b7EN)' },
    { v: '+140', l: '\u062d\u0648\u0627\u0631 \u062a\u0641\u0627\u0639\u0644\u064a' },
    { v: '+4000', l: '\u062a\u0645\u0631\u064a\u0646' },
    { v: 'AI', l: '\u0645\u062d\u0627\u062f\u062b\u0629 \u0630\u0643\u064a\u0629' },
  ]

  return (
    <main dir="rtl" style={{
      minHeight: '100vh', display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      background: 'var(--aq-gradient-hero)', position: 'relative',
      overflow: 'hidden', padding: '48px 24px',
      fontFamily: "var(--aq-font-arabic)",
    }}>
      {/* Radial glow */}
      <div style={{
        position: 'absolute', inset: 0, opacity: 0.5,
        background: 'radial-gradient(circle at 50% 30%, rgba(42,82,152,0.6), transparent 60%)',
        pointerEvents: 'none',
      }} />

      <div style={{ position: 'relative', zIndex: 10, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>

        {/* Logo */}
        <img src={logo} alt="Arabiq Akademi" width={140} height={140}
          style={{
            width: 140, height: 140,
            filter: 'drop-shadow(0 10px 40px rgba(201,168,76,0.35))',
            animation: 'aq-float-slow 6s ease-in-out infinite',
          }} />

        {/* AI Badge */}
        <div style={{
          marginTop: 32, display: 'inline-flex', alignItems: 'center', gap: 8,
          borderRadius: 999, border: '1px solid rgba(201,168,76,0.3)',
          background: 'rgba(201,168,76,0.1)', padding: '6px 18px',
          fontSize: 13, fontWeight: 500, color: '#D4B96A',
          backdropFilter: 'blur(4px)',
        }}>
          <span style={{ fontSize: 14 }}>{'\u2728'}</span>
          {'\u0645\u062f\u0639\u0648\u0645 \u0628\u0627\u0644\u0630\u0643\u0627\u0621 \u0627\u0644\u0627\u0635\u0637\u0646\u0627\u0639\u064a'}
        </div>

        {/* Title */}
        <h1 style={{
          marginTop: 28, fontSize: 'clamp(42px, 8vw, 72px)', fontWeight: 500,
          color: '#FAF8F3', fontFamily: "var(--aq-font-display)",
          lineHeight: 1.15, letterSpacing: '-0.02em',
        }}>
          Arabiq Akademi
        </h1>

        {/* Description */}
        <p style={{
          marginTop: 18, maxWidth: 520, fontSize: 'clamp(16px, 2.5vw, 20px)',
          lineHeight: 1.7, color: 'rgba(250,248,243,0.75)',
        }}>
          {'\u0645\u0646\u0635\u0629 \u062a\u0641\u0627\u0639\u0644\u064a\u0629 \u0644\u062a\u0639\u0644\u064a\u0645 \u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0639\u0631\u0628\u064a\u0629'}
          <br />
          <span style={{ color: '#D4B96A' }}>
            {'\u0644\u0637\u0644\u0627\u0628 \u0643\u0644\u064a\u0629 \u0627\u0644\u0625\u0644\u0647\u064a\u0627\u062a \u0648\u0645\u062a\u0639\u0644\u0651\u0645\u064a \u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0639\u0631\u0628\u064a\u0629'}
          </span>
        </p>

        {/* Turkish subtitle */}
        <p style={{ marginTop: 10, fontSize: 14, color: 'rgba(250,248,243,0.55)' }} lang="tr">
          {'\u0130lahiyat Fak\u00fcltesi \u00f6\u011frencileri ve Arap\u00e7a \u00f6\u011frenenler i\u00e7in'}
        </p>

        {/* University */}
        <p style={{ marginTop: 6, fontSize: 13, color: 'rgba(250,248,243,0.45)' }}>
          Karab&uuml;k &Uuml;niversitesi {'\u0130'}lahiyat Fak&uuml;ltesi
        </p>

        {/* CTA Button */}
        <Link to="/login" style={{
          marginTop: 40, display: 'inline-flex', alignItems: 'center', gap: 12,
          padding: '16px 36px', borderRadius: 999, fontSize: 17, fontWeight: 600,
          textDecoration: 'none',
          background: 'var(--aq-gradient-gold)',
          boxShadow: 'var(--aq-shadow-gold)',
          color: '#1a1a2e',
          fontFamily: "var(--aq-font-arabic)",
          transition: 'transform .2s, box-shadow .2s',
        }}
          onMouseEnter={e => { e.currentTarget.style.transform = 'scale(1.03)'; e.currentTarget.style.boxShadow = '0 14px 40px -10px rgba(201,168,76,0.6)' }}
          onMouseLeave={e => { e.currentTarget.style.transform = 'scale(1)'; e.currentTarget.style.boxShadow = 'var(--aq-shadow-gold)' }}
        >
          {'\u0627\u0628\u062f\u0623 \u0627\u0644\u0622\u0646'}
          <span style={{ fontSize: 16 }}>{'\u2190'}</span>
        </Link>

        {/* Stats */}
        <div style={{
          marginTop: 64, display: 'grid',
          gridTemplateColumns: 'repeat(5, 1fr)',
          gap: 'clamp(16px, 4vw, 40px)',
        }} className="aq-stats-grid">
          {stats.map(s => (
            <div key={s.l} style={{ textAlign: 'center' }}>
              <div style={{
                fontSize: 'clamp(22px, 3.5vw, 32px)', fontWeight: 600,
                color: '#C9A84C', fontFamily: "var(--aq-font-display)",
              }}>{s.v}</div>
              <div style={{
                marginTop: 4, fontSize: 'clamp(10px, 1.5vw, 13px)',
                color: 'rgba(250,248,243,0.6)',
              }}>{s.l}</div>
            </div>
          ))}
        </div>

      </div>

      <style>{`
        @media (max-width: 640px) {
          .aq-stats-grid { grid-template-columns: repeat(2, 1fr) !important; }
        }
      `}</style>
    </main>
  )
}
"""

landing_path = os.path.join(BASE, "pages", "Landing.jsx")
with open(landing_path, "w", encoding="utf-8") as f:
    f.write(LANDING)
print("✓ 1. أُنشئ Landing.jsx")

# ══════════════════════════════════════════════════════════
# 2. تعديل App.jsx لإضافة مسار Landing
# ══════════════════════════════════════════════════════════
app_path = os.path.join(BASE, "App.jsx")
app = open(app_path, encoding="utf-8").read()

# أضف import Landing
if "Landing" not in app:
    # أضف بعد آخر import
    last_import = app.rfind("import ")
    end_of_line = app.index("\n", last_import)
    app = app[:end_of_line+1] + "import Landing from './pages/Landing'\n" + app[end_of_line+1:]
    print("✓ 2a. أُضيف import Landing")

    # أضف Route للـ Landing قبل أول Route موجود
    # نبحث عن <Route الأولى ونضيف قبلها مسار Landing
    route_idx = app.find("<Route ")
    if route_idx > 0:
        # أضف مسار / يشير لـ Landing
        landing_route = '            <Route path="/landing" element={<Landing />} />\n'
        app = app[:route_idx] + landing_route + app[route_idx:]
        print("✓ 2b. أُضيف مسار /landing في الراوتر")

    open(app_path, "w", encoding="utf-8").write(app)
else:
    print("✓ 2. Landing موجود مسبقاً في App.jsx")

# اطبع المسارات الحالية
print("\n=== المسارات الحالية في App.jsx ===")
for line in app.split("\n"):
    if "Route" in line and "path" in line:
        print(f"  {line.strip()}")

print("\n✅ تم! الصفحة الترحيبية جاهزة على /landing")
print("   شغّلي: cd frontend && vercel --prod --yes")