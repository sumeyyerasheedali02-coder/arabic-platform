import { normalizeStudentNumber } from './studentNumber'

export default function StudentNumberField({ value, onChange, t }) {
  return <div style={{ marginBottom: 18 }}>
    <label htmlFor="student-number" style={{
      display: 'block', fontSize: 13, fontWeight: 600, color: 'var(--aq-text-muted)',
      marginBottom: 8, fontFamily: 'var(--aq-font-arabic)',
    }}>{t.studentNumber}</label>
    <input id="student-number" name="student_number" type="text" inputMode="numeric"
      autoComplete="off" dir="ltr" required maxLength={32} pattern="[0-9]{1,32}"
      value={value} onChange={event => onChange(normalizeStudentNumber(event.target.value))}
      placeholder={t.studentNumberPlaceholder} style={{
        width: '100%', padding: '14px 18px', borderRadius: 14,
        background: 'var(--aq-ivory)', border: '1.5px solid var(--aq-border)',
        color: 'var(--aq-text)', fontSize: 15, fontFamily: 'var(--aq-font-sans)',
      }} />
  </div>
}
