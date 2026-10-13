import { Link } from 'react-router-dom'

/** Navy banner with the unit title and the "add to review" action. */
export default function UnitHeader({ unit, canSave, message, onAddToReview }) {
  return (
    <div style={{
      background: 'var(--navy)', borderRadius: 14,
      padding: '18px 22px', marginBottom: 20, gap: 12, flexWrap: 'wrap',
      display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between',
    }}>
      <div>
        <div style={{ fontSize: 10, color: 'rgba(201,168,76,.7)', letterSpacing: '.06em', marginBottom: 4 }}>
          الوحدة {unit.unit_number}
        </div>
        <div style={{ fontFamily: "'Amiri', serif", fontSize: 20, color: '#fff', marginBottom: 2 }}>
          {unit.title_ar}
        </div>
        <div style={{ fontSize: 11, color: 'rgba(255,255,255,.45)' }}>{unit.title_tr}</div>
        {message && (
          <div style={{ marginTop: 8, fontSize: 11, color: '#C9A84C', background: 'rgba(201,168,76,.1)', borderRadius: 6, padding: '4px 10px', display: 'inline-block' }}>
            {message}
          </div>
        )}
      </div>
      {canSave ? (
        <button
          onClick={onAddToReview}
          style={{
            background: 'rgba(201,168,76,.15)', border: '1px solid rgba(201,168,76,.3)',
            color: '#C9A84C', borderRadius: 8, padding: '7px 14px',
            fontSize: 12, fontWeight: 500, cursor: 'pointer', flexShrink: 0,
            fontFamily: 'DM Sans, sans-serif',
          }}
        >
          + أضف للمراجعة
        </button>
      ) : (
        <Link
          to="/login"
          style={{
            fontSize: 11, color: 'rgba(201,168,76,.7)', textDecoration: 'underline',
            flexShrink: 0, fontFamily: 'DM Sans, sans-serif',
          }}
        >
          سجّل الدخول للإضافة
        </Link>
      )}
    </div>
  )
}
