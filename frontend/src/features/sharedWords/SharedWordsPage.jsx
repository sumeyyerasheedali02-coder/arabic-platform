import { useMemo, useState } from 'react'
import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import ErrorState from '../../components/ErrorState'
import { CenteredSpinner } from '../../components/Spinner'
import { filterWords, totalCount } from './sharedWords'
import './sharedWords.css'

const EMPTY = []
const PAGE_SIZE = 24
export default function SharedWordsPage() {
  const query = useApiData('shared-words', () => api.get('/shared-words').then(r => r.data))
  const [selectedCategory, setCategory] = useState(null)
  const [search, setSearch] = useState('')
  const [limit, setLimit] = useState(PAGE_SIZE)
  const [expanded, setExpanded] = useState(false)
  const categories = query.data?.categories ?? EMPTY
  const category = categories.some(c => c.key === selectedCategory) ? selectedCategory : categories[0]?.key ?? ''
  const words = useMemo(() => filterWords(categories, category, search), [categories, category, search])
  function choose(value) { setCategory(value); setLimit(PAGE_SIZE) }
  if (query.loading) return <CenteredSpinner size={32} height={260} />
  if (query.error) return <ErrorState onRetry={query.reload} />
  return <div className="cognates-page" dir="rtl">
    <header className="cognates-hero"><span className="cognates-eyebrow">العربية × Türkçe</span><h1>كلمات تعرفها بالفعل</h1><p>اكتشف ما يجمع العربية والتركية، وانتبه لاختلاف المعنى.</p><span className="cognates-total" lang="tr" dir="ltr">{totalCount(categories)} ortak kelime</span></header>
    <section className="cognates-tools" aria-label="البحث والتصنيف">
      <div className="cognates-search"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true"><circle cx="10.5" cy="10.5" r="7"/><path d="m16 16 5 5"/></svg><input type="search" value={search} onChange={e => { setSearch(e.target.value); setLimit(PAGE_SIZE) }} dir="auto" placeholder="ابحث بكلمة عربية أو تركية…" aria-label="بحث في المفردات المشتركة" /></div>
      <label className="cognates-mobile-category" htmlFor="cognates-category">التصنيف<select id="cognates-category" value={category} onChange={e => choose(e.target.value)}>{categories.map(c => <option key={c.key} value={c.key}>{c.title_ar} ({c.words.length})</option>)}</select></label>
      <div className="cognates-categories" id="cognates-categories" role="group" aria-label="تصنيفات الكلمات">{categories.filter((c,index) => expanded || index < 5 || c.key === category).map(c => <button key={c.key} aria-pressed={category === c.key} onClick={() => choose(c.key)}>{c.title_ar}<span>{c.words.length}</span></button>)}</div>
      {categories.length > 5 && <button className="cognates-category-toggle" aria-expanded={expanded} aria-controls="cognates-categories" onClick={() => setExpanded(value => !value)}>{expanded ? 'اختصار التصنيفات ↑' : `جميع التصنيفات (${categories.length}) ↓`}</button>}
    </section>
    <div className="cognates-results-title"><h2>{categories.find(c => c.key === category)?.title_ar ?? 'المفردات المشتركة'}</h2><span role="status" aria-live="polite">{words.length} نتيجة</span></div>
    {words.length ? <><div className="cognates-grid">{words.slice(0,limit).map((word, index) => <article className="cognate-card" key={`${word.category}:${word.ar}:${word.tr}:${index}`}>
      <div className="cognate-meta"><span>{word.category_ar}</span><span className={`cognate-usage${word.usage === 'تراثية' ? ' is-literary' : ''}`}>{word.usage}</span></div>
      <div className="cognate-pair"><div><span>العربية</span><h3 lang="ar" dir="rtl">{word.ar}</h3></div><span className="cognate-bridge" aria-hidden="true">↔</span><div lang="tr" dir="ltr"><span>Türkçe</span><p>{word.tr}</p></div></div>
      {word.note && <p className="cognate-note"><strong>انتبه للمعنى</strong>{word.note}</p>}
    </article>)}</div><div className="cognates-more"><span>عرض {Math.min(limit,words.length)} من {words.length}</span>{limit < words.length && <button onClick={() => setLimit(value => value + PAGE_SIZE)}>عرض المزيد <span aria-hidden="true">↓</span></button>}</div></> : <div className="cognates-empty"><h3>لا توجد كلمات مطابقة</h3><p>جرّب كلمة أخرى أو اختر تصنيفًا آخر.</p><button onClick={() => { setSearch(''); setLimit(PAGE_SIZE) }}>مسح البحث</button></div>}
  </div>
}
