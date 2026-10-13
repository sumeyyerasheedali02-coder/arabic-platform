import { lessonColor, lessonLabel } from './lessonTypes'

/** One lesson in the unit's grid; opens the lesson panel. */
export default function LessonCard({ lesson, onOpen }) {
  const dotColor = lessonColor(lesson)
  return (
    <button
      onClick={() => onOpen(lesson)}
      style={{
        background: '#fff', border: '1px solid var(--border)', borderRadius: 12,
        padding: '16px 18px', textAlign: 'right', cursor: 'pointer',
        transition: 'all .18s', fontFamily: 'DM Sans, sans-serif',
        display: 'flex', gap: 12, alignItems: 'flex-start',
        boxShadow: '0 1px 3px rgba(0,0,0,.04)',
      }}
      onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--gold)'; e.currentTarget.style.boxShadow = '0 4px 12px rgba(15,32,68,.08)' }}
      onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,.04)' }}
    >
      <div style={{
        width: 36, height: 36, borderRadius: 9, flexShrink: 0,
        background: `${dotColor}18`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        border: `1px solid ${dotColor}30`,
      }}>
        <div style={{ width: 8, height: 8, borderRadius: '50%', background: dotColor }} />
      </div>
      <div style={{ flex: 1, minWidth: 0, textAlign: 'right' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 4 }}>
          <span style={{
            fontSize: 10, color: dotColor, fontWeight: 600,
            background: `${dotColor}15`, borderRadius: 4, padding: '1px 6px',
          }}>
            {lessonLabel(lesson)}
          </span>
          <span style={{ fontSize: 10, color: 'var(--muted)' }}>
            درس {lesson.lesson_number}
          </span>
        </div>
        <div style={{ fontFamily: "'Amiri', serif", fontSize: 15, color: 'var(--navy)', lineHeight: 1.4 }}>
          {lesson.title_ar}
        </div>
        {lesson.title_tr && (
          <div style={{ fontSize: 11, color: 'var(--muted)', marginTop: 2 }}>
            {lesson.title_tr}
          </div>
        )}
        {lesson.grammar_focus && (
          <div style={{ fontSize: 11, color: '#7c3aed', marginTop: 5, fontFamily: "'Amiri', serif" }}>
            {lesson.grammar_focus.split('|')[0].trim()}...
          </div>
        )}
      </div>
      <div style={{ color: 'var(--muted)', fontSize: 14, marginTop: 8, flexShrink: 0 }}>›</div>
    </button>
  )
}
