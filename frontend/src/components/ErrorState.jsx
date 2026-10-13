export const LOAD_ERROR_MESSAGE = 'تعذّر تحميل البيانات. تحقق من اتصالك بالإنترنت ثم حاول مرة أخرى.'

/** Shown instead of content when a request failed. `compact` fits inside panels and cards. */
export default function ErrorState({ onRetry, compact = false, message = LOAD_ERROR_MESSAGE }) {
  return (
    <div role="alert" style={{
      maxWidth: 420, textAlign: 'center',
      margin: compact ? '0 auto' : '60px auto',
      padding: compact ? '24px 0' : '0 16px',
    }}>
      <div style={{ fontSize: compact ? 28 : 44, marginBottom: 10 }}>⚠️</div>
      <p style={{ color: 'var(--muted)', fontSize: 13, lineHeight: 1.6, marginBottom: onRetry ? 16 : 0 }}>
        {message}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          style={{
            background: 'var(--navy)', color: '#fff', border: 'none', cursor: 'pointer',
            borderRadius: 9, padding: '10px 28px', fontWeight: 500, fontSize: 13,
            fontFamily: 'DM Sans, sans-serif',
          }}
        >
          إعادة المحاولة
        </button>
      )}
    </div>
  )
}
