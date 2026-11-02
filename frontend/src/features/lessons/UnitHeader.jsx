import { Link } from 'react-router-dom'

function UnitIcon({ name }) {
  const paths = {
    book: <><path d="M12 5c-3-2-6-2-10-1v15c4-1 7-1 10 1 3-2 6-2 10-1V4c-4-1-7-1-10 1Z" /><path d="M12 5v15" /></>,
    words: <><path d="M3 5h12M9 3v2M5 5c1 6 5 9 9 11M13 5c-1 5-5 9-10 12M14 21l4-10 4 10M15.5 18h5" /></>,
    clock: <><circle cx="12" cy="12" r="9" /><path d="M12 6v6l4 3" /></>,
    target: <><circle cx="11" cy="13" r="8" /><circle cx="11" cy="13" r="4" /><path d="m11 13 9-10M16 3h4v4" /></>,
    plus: <path d="M12 4v16M4 12h16" />,
  }
  return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name]}</svg>
}

/** Decorative unit artwork; all counts and progress come from loaded content. */
export default function UnitHeader({ unit, lessonCount, vocabularyCount, progressPercent, studySeconds, canSave, message, onAddToReview, onShowVocabulary, preview = false }) {
  const number = Number(unit.unit_number)
  const showMoreArtwork = [9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 26, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 44, 45, 46, 47].includes(number)
  const artwork = Number.isInteger(number) && number >= 1 && number <= 48
    ? `${import.meta.env.BASE_URL}images/units/unit-${String(number).padStart(2, '0')}-scene` : null
  const percent = Number.isFinite(progressPercent) ? Math.max(0, Math.min(100, Math.round(progressPercent))) : null
  return (
    <section className={`unit-header unit-header--scene${showMoreArtwork ? ' unit-header--wide-scene' : ''}${number === 20 ? ' unit-header--city' : ''}`} aria-labelledby="unit-title">
      {artwork && <div className="unit-header-art-window" style={showMoreArtwork ? { '--unit-scene-backdrop': `url("${artwork}-small.webp?v=2")` } : undefined}><img className="unit-header-art" src={`${artwork}.webp?v=2`} srcSet={`${artwork}-small.webp?v=2 960w, ${artwork}.webp?v=2 1448w`} sizes="(max-width: 768px) 100vw, 750px" alt="" width={1448} height={1086} decoding="async" /></div>}
      <div className="unit-header-copy">
        <div className="unit-header-summary">
        <div className="unit-header-number">الوحدة {unit.unit_number}</div>
        <h1 id="unit-title" className="unit-header-title">{unit.title_ar}</h1>
        <div className="unit-header-translation" lang="tr" dir="ltr">{unit.title_tr}</div>
        </div>
        <div className="unit-header-facts" aria-label="محتوى الوحدة">
          {Number.isInteger(lessonCount) && lessonCount >= 0 && <span><UnitIcon name="book" /><span><strong>{lessonCount}</strong> دروس</span></span>}
          {Number.isInteger(vocabularyCount) && vocabularyCount >= 0 && <span><UnitIcon name="words" /><span><strong>{vocabularyCount}</strong> كلمة</span></span>}
          {Number.isFinite(studySeconds) && <span title="وقت الدراسة المسجّل لهذه الوحدة"><UnitIcon name="clock" /><span><strong>{Math.floor(studySeconds / 60)}</strong> دقيقة</span></span>}
        </div>
      </div>
      <div className="unit-header-tools">
        <div className={`unit-progress${percent === null ? ' is-unknown' : ''}`} style={{ '--unit-completion': `${percent ?? 0}%` }} role={percent === null ? 'group' : 'progressbar'} aria-label={percent === null ? 'سجّل الدخول لعرض تقدّمك' : 'إنجاز دروس الوحدة'} aria-valuemin={percent === null ? undefined : 0} aria-valuemax={percent === null ? undefined : 100} aria-valuenow={percent ?? undefined}>
          <svg viewBox="0 0 112 112" aria-hidden="true"><circle className="unit-progress-track" cx="56" cy="56" r="48" /><circle className="unit-progress-value" cx="56" cy="56" r="48" pathLength="100" strokeDasharray={`${percent ?? 0} 100`} /></svg>
          <div><strong dir="ltr">{percent === null ? '—' : `${percent}%`}</strong><span>{percent === null ? (preview ? 'معاينة المحتوى' : 'سجّل دخولك') : 'تم الإنجاز'}</span></div>
        </div>
        <div className="unit-header-actions">
          <button className="unit-action-primary" onClick={onShowVocabulary}><UnitIcon name="target" />تابع المفردات</button>
          {canSave ? <button className="unit-action-secondary" onClick={onAddToReview}><UnitIcon name="plus" />أضف للمراجعة</button> : !preview && <Link className="unit-action-secondary" to="/login"><UnitIcon name="plus" />أضف للمراجعة</Link>}
        </div>
      </div>
      {message && <div className="unit-header-message" role="status">{message}</div>}
    </section>
  )
}
