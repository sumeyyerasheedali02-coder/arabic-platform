const OPTIONS = [
  { code: 'ar', label: 'العربية', font: 'var(--aq-font-arabic)' },
  { code: 'tr', label: 'Türkçe', font: 'var(--aq-font-sans)' },
]

/** Arabic / Turkish pill switch of the login page. */
export default function LanguageSwitch({ lang, onChange }) {
  return (
    <div className="langSw" style={{
      display: 'inline-flex', borderRadius: 999, border: '1px solid var(--aq-border)',
      background: 'var(--aq-card)', padding: 3, fontSize: 13, fontWeight: 500,
      boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
    }}>
      {OPTIONS.map(({ code, label, font }) => (
        <button key={code} type="button" onClick={() => onChange(code)}
          style={{
            borderRadius: 999, padding: '6px 14px', border: 'none', cursor: 'pointer',
            transition: 'all .2s', fontFamily: font,
            background: lang === code ? 'var(--aq-navy)' : 'transparent',
            color: lang === code ? '#FAF8F3' : 'var(--aq-text-muted)',
            boxShadow: lang === code ? '0 2px 6px rgba(15,32,68,0.3)' : 'none',
          }}>
          {label}
        </button>
      ))}
    </div>
  )
}
