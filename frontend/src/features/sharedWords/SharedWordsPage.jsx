import { useMemo, useState } from 'react'
import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import ErrorState from '../../components/ErrorState'
import { CenteredSpinner } from '../../components/Spinner'
import { filterWords, totalCount } from './sharedWords'

const NO_CATEGORIES = []

// شائعة = still common in Turkish today; تراثية = archaic/literary.
const USAGE_STYLE = {
  شائعة: { background: 'rgba(46,125,50,.1)', color: '#2E7D32' },
  تراثية: { background: 'rgba(146,110,30,.12)', color: '#926E1E' },
}

/**
 * «مفردات مشتركة» — Arabic words that a Turkish speaker already half-knows,
 * grouped by topic. Each row shows the Arabic form, the Turkish cognate, how
 * common it is, and a note when the meaning differs (false friends). Public.
 */
export default function SharedWordsPage() {
  const query = useApiData('shared-words', () => api.get('/shared-words').then(r => r.data))
  const [category, setCategory] = useState('all')
  const [search, setSearch] = useState('')

  const categories = query.data?.categories ?? NO_CATEGORIES
  const total = query.data?.total ?? 0
  const words = useMemo(
    () => filterWords(categories, category, search),
    [categories, category, search],
  )

  if (query.loading) return <CenteredSpinner size={32} height={260} />
  if (query.error) return <ErrorState onRetry={query.reload} />

  return (
    <div style={{ maxWidth: 900, margin: '0 auto', padding: '24px 16px 48px' }}>
      {/* Heading */}
      <div style={{ marginBottom: 6 }}>
        <h1 style={{ fontFamily: "'Amiri', serif", fontSize: 26, color: 'var(--navy)', margin: 0 }}>
          المفردات المشتركة
        </h1>
        <p style={{ fontSize: 13, color: 'var(--muted)', margin: '6px 0 0', lineHeight: 1.7 }}>
          كلماتٌ عربيةٌ تشاركها التركية في اللفظ أو الجذر — تعرفها أنت أصلًا.
          انتبه لملاحظات فروق المعنى؛ فبعضها «أصدقاء كاذبون» يختلف معناها في التركية.
        </p>
        <p className="shared-count" style={{ fontSize: 11, color: 'var(--muted)', margin: '4px 0 0' }} dir="ltr">
          {totalCount(categories)} / {total}
        </p>
      </div>

      {/* Search */}
      <input
        type="search"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="ابحث بالعربية أو التركية…"
        aria-label="بحث في المفردات المشتركة"
        style={{
          width: '100%', boxSizing: 'border-box', margin: '16px 0 12px',
          padding: '10px 14px', borderRadius: 9, border: '1px solid var(--border)',
          fontSize: 14, fontFamily: "'Amiri', serif", background: '#fff', color: 'var(--text)',
        }}
      />

      {/* Category chips */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 18 }}>
        <Chip active={category === 'all'} onClick={() => setCategory('all')}>الكل</Chip>
        {categories.map((c) => (
          <Chip key={c.key} active={category === c.key} onClick={() => setCategory(c.key)}>
            {c.title_ar}
          </Chip>
        ))}
      </div>

      {/* Results */}
      {words.length === 0 ? (
        <p style={{ textAlign: 'center', color: 'var(--muted)', fontSize: 13, padding: '40px 0' }}>
          لا توجد نتائج مطابقة.
        </p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {words.map((w, i) => (
            <div
              key={`${w.category}:${w.ar}:${w.tr}:${i}`}
              style={{
                display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap',
                background: '#fff', border: '1px solid var(--border)', borderRadius: 11,
                padding: '12px 16px',
              }}
            >
              <div style={{ fontFamily: "'Amiri', serif", fontSize: 20, color: 'var(--navy)', minWidth: 110 }}>
                {w.ar}
              </div>
              <div dir="ltr" style={{ fontSize: 15, fontWeight: 500, color: 'var(--text)', minWidth: 110, textAlign: 'left' }}>
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
      )}
    </div>
  )
}

function Chip({ active, onClick, children }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: '5px 12px', borderRadius: 20, fontSize: 11.5, fontWeight: 500, cursor: 'pointer',
        border: '1px solid ' + (active ? 'var(--navy)' : 'var(--border)'),
        background: active ? 'var(--navy)' : '#fff',
        color: active ? '#fff' : 'var(--muted)',
        fontFamily: "'Amiri', serif", transition: 'all .15s',
      }}
    >
      {children}
    </button>
  )
}
