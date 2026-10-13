const ACADEMIC_TAG = { display: 'inline-flex', alignItems: 'center', gap: 8, fontSize: 12, fontWeight: 600, letterSpacing: '0.15em', color: '#C9A84C', marginBottom: 8 }
const TAG_LINE = { width: 32, height: 1, background: '#C9A84C', display: 'inline-block' }

function AcademicTag() {
  return (
    <div style={ACADEMIC_TAG}>
      <span style={TAG_LINE} />أكاديمي
    </div>
  )
}

function Badge({ emoji, background, border }) {
  return (
    <div style={{
      width: 56, height: 56, borderRadius: 16, background,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontSize: 28, margin: '0 auto 12px', border: `1px solid ${border}`,
    }}>{emoji}</div>
  )
}

/**
 * Heading of the login card. `emailState` is the step of the flow:
 * idle / checking (e-mail not looked up yet), existing (log in), new (register).
 */
export default function CardHeading({ emailState, t }) {
  if (emailState === 'existing') {
    return (
      <div style={{ textAlign: 'center', marginBottom: 28, animation: 'aq-fade-in .3s ease-out' }}>
        <Badge emoji="👋" background="#F0FDF4" border="#BBF7D0" />
        <h2 style={{ fontSize: 22, fontWeight: 800, color: 'var(--aq-navy)' }}>{t.welcome}</h2>
        <p style={{ fontSize: 13, color: 'var(--aq-text-muted)', marginTop: 4 }}>{t.enterPwd}</p>
      </div>
    )
  }
  if (emailState === 'new') {
    return (
      <div style={{ textAlign: 'center', marginBottom: 28, animation: 'aq-fade-in .3s ease-out' }}>
        <Badge emoji="🎓" background="#EFF6FF" border="#BFDBFE" />
        <AcademicTag />
        <h2 style={{ fontSize: 22, fontWeight: 800, color: 'var(--aq-navy)' }}>{t.newAccount}</h2>
        <p style={{ fontSize: 13, color: 'var(--aq-text-muted)', marginTop: 4 }}>{t.newSub}</p>
      </div>
    )
  }
  return (
    <div style={{ textAlign: 'center', marginBottom: 28 }}>
      <AcademicTag />
      <h2 style={{ fontSize: 28, fontWeight: 700, color: 'var(--aq-navy)' }}>
        {emailState === 'checking' ? 'جارٍ التحقق...' : t.title}
      </h2>
      <p style={{ fontSize: 13, color: 'var(--aq-text-muted)', marginTop: 6 }}>{t.subtitle}</p>
    </div>
  )
}
