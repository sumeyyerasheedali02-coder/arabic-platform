import { Link } from 'react-router-dom'

/** End-of-session screen with the three result tiles. */
export default function SessionSummary({ total, correctCount, pct, totalPoints, isGuest, onRestart }) {
  return (
    <div style={{ maxWidth: 440, margin: '0 auto', padding: '60px 16px', textAlign: 'center' }}>
      <div style={{ fontSize: 64, marginBottom: 16 }}>{pct >= 80 ? '🏆' : pct >= 50 ? '👏' : '💪'}</div>
      <h1 style={{ fontSize: 22, fontWeight: 700, color: 'var(--navy)', marginBottom: 8 }}>انتهت جلسة التمارين!</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 10, margin: '24px 0' }}>
        {[['📝', total, 'تمرين'], ['✅', correctCount, 'صحيح'], ['📊', `${pct}%`, 'نجاح']].map(([icon, val, label]) => (
          <div key={label} style={{ background: '#fff', borderRadius: 14, padding: '14px 10px', border: '1px solid var(--border)' }}>
            <div style={{ fontSize: 22, marginBottom: 4 }}>{icon}</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: 'var(--navy)' }}>{val}</div>
            <div style={{ fontSize: 11, color: 'var(--muted)' }}>{label}</div>
          </div>
        ))}
      </div>
      {isGuest && (
        <p style={{ fontSize: 12, color: 'var(--muted)', marginBottom: 12 }}>
          سجّل الدخول لحفظ نتائجك —{' '}
          <Link to="/login" style={{ color: 'var(--navy)', textDecoration: 'underline' }}>تسجيل الدخول</Link>
        </p>
      )}
      {!isGuest && (
        <p style={{ fontSize: 13, color: 'var(--muted)', marginBottom: 16 }}>
          مجموع النقاط: <span style={{ fontWeight: 700, color: 'var(--navy)' }}>{totalPoints}</span>
        </p>
      )}
      <button onClick={onRestart} style={{
        background: 'var(--navy)', color: '#fff', border: 'none', cursor: 'pointer',
        borderRadius: 10, padding: '11px 32px', fontWeight: 600, fontSize: 14,
        fontFamily: 'DM Sans, sans-serif',
      }}>
        حاول مرة اخرى
      </button>
    </div>
  )
}
