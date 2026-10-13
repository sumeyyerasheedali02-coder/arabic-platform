const AMIRI = "'Amiri', serif"

// The same word row appears in three places with slightly different dressing.
const VARIANTS = {
  // lesson panel, "الدروس" tab of a vocabulary lesson: Turkish only, on one line
  compact: {
    row: { padding: '10px 14px', background: 'var(--cream)' },
    wordSize: 18, badgeBackground: 'var(--cream2)', exampleMarginTop: 3,
    english: false,
  },
  // lesson panel, "المفردات" tab
  panel: {
    row: { padding: '10px 14px', background: 'var(--cream)' },
    wordSize: 18, badgeBackground: '#fff', exampleMarginTop: 3,
    english: true, translationMarginRight: 12,
  },
  // lessons page, "المفردات" tab of the unit
  page: {
    row: { padding: '11px 16px', background: '#fff', gap: 12 },
    wordSize: 19, badgeBackground: 'var(--cream)', exampleMarginTop: 2,
    english: true,
  },
}

export default function VocabularyRow({ word, variant }) {
  const look = VARIANTS[variant]
  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      border: '1px solid var(--border)', borderRadius: 10,
      ...look.row,
    }}>
      <div>
        <span style={{ fontFamily: AMIRI, fontSize: look.wordSize, color: 'var(--navy)' }}>
          {word.word_ar}
        </span>
        {word.word_type && (
          <span style={{
            marginRight: 8, fontSize: 10, color: 'var(--muted)',
            background: look.badgeBackground, border: '1px solid var(--border)',
            borderRadius: 4, padding: '1px 6px',
          }}>
            {word.word_type}
          </span>
        )}
        {word.example_ar && (
          <div style={{ fontSize: 12, color: 'var(--muted)', marginTop: look.exampleMarginTop, fontFamily: AMIRI }}>
            {word.example_ar}
          </div>
        )}
      </div>
      {look.english ? (
        <div style={{
          textAlign: 'left', flexShrink: 0,
          ...(look.translationMarginRight ? { marginRight: look.translationMarginRight } : {}),
        }}>
          <div style={{ fontSize: 13, fontWeight: 500, color: 'var(--navy)' }} dir="ltr">
            {word.translation_tr}
          </div>
          {word.translation_en && (
            <div style={{ fontSize: 11, color: 'var(--muted)' }} dir="ltr">{word.translation_en}</div>
          )}
        </div>
      ) : (
        <span style={{ fontSize: 12, color: 'var(--navy)', fontWeight: 500, flexShrink: 0, marginRight: 10 }} dir="ltr">
          {word.translation_tr}
        </span>
      )}
    </div>
  )
}

/** A vertical list of word rows. */
export function VocabularyList({ words, variant }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
      {words.map(word => <VocabularyRow key={word.id} word={word} variant={variant} />)}
    </div>
  )
}
