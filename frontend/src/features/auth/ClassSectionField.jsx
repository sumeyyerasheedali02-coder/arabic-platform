import { CLASS_SECTIONS } from './texts'

/** The same explicit section choice for new students and existing accounts. */
export default function ClassSectionField({ value, onChange, t }) {
  return (
    <div style={{ marginBottom: 18 }}>
      <label htmlFor="class-section" style={{
        display: 'block', fontSize: 13, fontWeight: 600,
        color: 'var(--aq-text-muted)', marginBottom: 8,
        fontFamily: 'var(--aq-font-arabic)',
      }}>
        {t.classSection}
      </label>
      <select
        id="class-section" name="class_section" required
        value={value} onChange={e => onChange(e.target.value)}
        style={{
          width: '100%', padding: '14px 18px', borderRadius: 14,
          background: 'var(--aq-ivory)', border: '1.5px solid var(--aq-border)',
          color: 'var(--aq-text)', fontSize: 15, fontFamily: 'var(--aq-font-sans)',
          cursor: 'pointer', appearance: 'auto',
        }}
      >
        <option value="" disabled>{t.chooseSection}</option>
        {CLASS_SECTIONS.map(section => (
          <option key={section} value={section}>{t.classSection} {section}</option>
        ))}
      </select>
    </div>
  )
}
