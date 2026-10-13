const SECTION_LABEL = { fontSize: 10, color: 'var(--muted)', letterSpacing: '.08em', marginBottom: 12, fontWeight: 500 }

/** The grammar points of a lesson. The backend stores them as one string separated by "|". */
export default function GrammarRules({ grammarFocus }) {
  return (
    <div style={{ marginBottom: 20 }}>
      <div style={SECTION_LABEL}>القواعد النحوية — GRAMMAR</div>
      {grammarFocus.split('|').map((rule, i) => (
        <div key={i} style={{
          background: '#f5f3ff', border: '1px solid #ddd6fe',
          borderRadius: 10, padding: '12px 16px', marginBottom: 8,
          display: 'flex', gap: 12, alignItems: 'flex-start',
        }}>
          <div style={{
            width: 22, height: 22, borderRadius: '50%', flexShrink: 0,
            background: '#7c3aed', color: '#fff',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 10, fontWeight: 700,
          }}>
            {i + 1}
          </div>
          <div style={{ fontFamily: "'Amiri', serif", fontSize: 16, color: '#4c1d95', lineHeight: 1.6, direction: 'rtl' }}>
            {rule.trim()}
          </div>
        </div>
      ))}
    </div>
  )
}
