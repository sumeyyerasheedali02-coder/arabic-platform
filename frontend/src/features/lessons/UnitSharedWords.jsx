import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import ErrorState from '../../components/ErrorState'
import { CenteredSpinner } from '../../components/Spinner'

const NO_WORDS = []

// شائعة = still common in Turkish today; تراثية = archaic/literary.
const USAGE_STYLE = {
  شائعة: { background: 'rgba(46,125,50,.1)', color: '#2E7D32' },
  تراثية: { background: 'rgba(146,110,30,.12)', color: '#926E1E' },
}

/**
 * «كلمات مشتركة» tab of a unit: Arabic words on the unit's topic that Turkish
 * shares, so the student meets familiar sounds first. The unit is asked for by
 * its number, which is the same in every database.
 */
export default function UnitSharedWords({ unitNumber }) {
  const query = useApiData(
    `unit-shared-words:${unitNumber}`,
    () => api.get(`/shared-words/units/${unitNumber}`).then(r => r.data),
  )

  if (query.loading) return <CenteredSpinner size={28} padding={40} />
  if (query.error) return <ErrorState compact onRetry={query.reload} />
  const words = query.data?.words ?? NO_WORDS

  return (
    <div>
      <p style={{ fontSize: 12.5, color: 'var(--muted)', margin: '0 0 12px', lineHeight: 1.7 }}>
        كلماتٌ في موضوع هذه الوحدة تشاركها التركية في اللفظ أو الجذر — تعرف أصواتها أصلًا.
        انتبه لملاحظات فروق المعنى؛ فبعضها «أصدقاء كاذبون» يختلف معناها في التركية.
      </p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
        {words.map(w => (
          <div
            key={`${w.ar}:${w.tr}`}
            style={{
              display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap',
              background: '#fff', border: '1px solid var(--border)', borderRadius: 10,
              padding: '10px 16px',
            }}
          >
            <div style={{ fontFamily: "'Amiri', serif", fontSize: 19, color: 'var(--navy)', minWidth: 100 }}>
              {w.ar}
            </div>
            <div dir="ltr" style={{ fontSize: 14, fontWeight: 500, color: 'var(--text)', minWidth: 100, textAlign: 'left' }}>
              {w.tr}
            </div>
            <span style={{
              fontSize: 10, fontWeight: 600, padding: '2px 9px', borderRadius: 20,
              ...(USAGE_STYLE[w.usage] || USAGE_STYLE['شائعة']),
            }}>
              {w.usage}
            </span>
            {w.note && (
              <div style={{ flex: 1, minWidth: 180, fontSize: 12, color: 'var(--muted)', lineHeight: 1.6 }}>
                {w.note}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
