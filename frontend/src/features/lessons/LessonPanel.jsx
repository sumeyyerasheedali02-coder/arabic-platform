import { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'
import { useNavigate } from 'react-router-dom'
import api from '../../api/client'
import { CenteredSpinner } from '../../components/Spinner'
import { DialogueBubbles, DialogueScript } from './DialogueViews'
import GrammarRules from './GrammarRules'
import { VocabularyList } from './VocabularyRow'
import { lessonColor, lessonLabel } from './lessonTypes'

const TABS = [
  { key: 'lessons', label: 'الدروس' },
  { key: 'hiwar',   label: 'الحوار' },
  { key: 'vocab',   label: 'المفردات' },
]

const SECTION_LABEL = { fontSize: 10, color: 'var(--muted)', letterSpacing: '.08em', fontWeight: 500 }
const EMPTY_NOTE = { color: 'var(--muted)', textAlign: 'center', padding: '40px 0', fontSize: 13 }

function PanelHeader({ lesson, onBack }) {
  return (
    <div style={{
      padding: '12px 20px 14px', borderBottom: '1px solid var(--border)',
      background: 'var(--navy)', flexShrink: 0,
    }}>
      {/* Back button row */}
      <button
        onClick={onBack}
        style={{
          display: 'flex', alignItems: 'center', gap: 6,
          background: 'none', border: 'none', cursor: 'pointer',
          color: 'rgba(255,255,255,.55)', fontSize: 12, marginBottom: 10,
          fontFamily: 'DM Sans, sans-serif', padding: 0,
        }}
        onMouseEnter={e => e.currentTarget.style.color = '#C9A84C'}
        onMouseLeave={e => e.currentTarget.style.color = 'rgba(255,255,255,.55)'}
      >
        <span style={{ fontSize: 14 }}>←</span>
        <span>العودة إلى الدروس</span>
      </button>

      {/* Title row */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 10 }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
            <span style={{
              display: 'inline-block', width: 8, height: 8,
              borderRadius: '50%', background: lessonColor(lesson), flexShrink: 0,
            }} />
            <span style={{ fontSize: 11, color: 'rgba(255,255,255,.5)', letterSpacing: '.05em' }}>
              {lessonLabel(lesson)} · درس {lesson.lesson_number}
            </span>
          </div>
          <h2 style={{ fontFamily: "'Amiri', serif", fontSize: 18, color: '#fff', lineHeight: 1.3 }}>
            {lesson.title_ar}
          </h2>
          {lesson.title_tr && (
            <p style={{ fontSize: 11, color: 'rgba(255,255,255,.45)', marginTop: 3 }}>{lesson.title_tr}</p>
          )}
        </div>
        <button
          onClick={onBack}
          style={{
            background: 'rgba(255,255,255,.1)', border: 'none', cursor: 'pointer',
            width: 28, height: 28, borderRadius: 6,
            color: '#fff', fontSize: 16, display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexShrink: 0,
          }}
        >
          ×
        </button>
      </div>
    </div>
  )
}

function PanelTabs({ active, onChange }) {
  return (
    <div style={{
      display: 'flex', borderBottom: '1px solid var(--border)',
      background: '#fff', padding: '0 20px', gap: 4,
      overflowX: 'auto', flexShrink: 0,
    }}>
      {TABS.map(({ key, label }) => (
        <button
          key={key}
          onClick={() => onChange(key)}
          className={active === key ? 'tab-active' : 'tab-inactive'}
          style={{
            padding: '10px 14px', fontSize: 12.5, fontWeight: 500,
            background: 'none', border: 'none', cursor: 'pointer',
            fontFamily: 'DM Sans, sans-serif', transition: 'all .15s',
          }}
        >
          {label}
        </button>
      ))}
    </div>
  )
}

/** "الدروس" tab: what is shown depends on the kind of lesson. */
function LessonTab({ lesson, words, dialogues, loading }) {
  const navigate = useNavigate()
  const type = lesson.lesson_type
  return (
    <div>
      {lesson.grammar_focus && <GrammarRules grammarFocus={lesson.grammar_focus} />}

      {type === 'mufradat' && words.length > 0 && (
        <>
          <div style={{ ...SECTION_LABEL, marginBottom: 12 }}>المفردات — VOCABULARY</div>
          <VocabularyList words={words} variant="compact" />
        </>
      )}

      {type === 'hiwar' && (
        loading ? (
          <CenteredSpinner size={24} padding={40} />
        ) : dialogues.length === 0 ? (
          <p style={EMPTY_NOTE}>لا يوجد نص لهذا الحوار بعد</p>
        ) : (
          <DialogueScript dialogues={dialogues} />
        )
      )}

      {(type === 'tadrib' || type === 'aswat') && (
        <div style={{
          background: '#fff7ed', border: '1px solid #fed7aa', borderRadius: 12,
          padding: 24, textAlign: 'center',
        }}>
          <div style={{ fontSize: 36, marginBottom: 10 }}>✏️</div>
          <div style={{ fontSize: 15, fontWeight: 600, color: '#92400e', marginBottom: 6 }}>
            تدريبات هذا الدرس
          </div>
          <div style={{ fontSize: 12, color: '#b45309', marginBottom: 16 }}>
            افتح صفحة التمارين لحل التدريبات الخاصة بهذه الوحدة
          </div>
          <button
            onClick={() => navigate('/exercises')}
            style={{
              background: '#92400e', color: '#fff', border: 'none', cursor: 'pointer',
              borderRadius: 8, padding: '8px 22px', fontWeight: 500, fontSize: 13,
              fontFamily: 'DM Sans, sans-serif',
            }}
          >
            اذهب إلى التمارين
          </button>
        </div>
      )}

      {type === 'nahw' && !lesson.grammar_focus && (
        <p style={EMPTY_NOTE}>لا توجد قواعد نحوية مدخلة لهذا الدرس بعد</p>
      )}
    </div>
  )
}

function DialogueTab({ dialogues, loading }) {
  return (
    <div>
      {loading ? (
        <CenteredSpinner size={24} padding={40} />
      ) : dialogues.length === 0 ? (
        <p style={EMPTY_NOTE}>لا يوجد حوار لهذا الدرس</p>
      ) : (
        <DialogueBubbles dialogues={dialogues} />
      )}
    </div>
  )
}

function VocabularyTab({ words }) {
  return (
    <div>
      <div style={{ ...SECTION_LABEL, marginBottom: 14 }}>مفردات الوحدة — VOCABULARY</div>
      {words.length === 0 ? (
        <p style={EMPTY_NOTE}>لا توجد مفردات مرتبطة بهذا الدرس</p>
      ) : (
        <>
          {/* Chips row */}
          <div style={{ display: 'flex', flexWrap: 'wrap', marginBottom: 18 }}>
            {words.map(v => (
              <span
                key={v.id}
                style={{
                  display: 'inline-block',
                  background: 'var(--cream)', border: '1px solid var(--border)',
                  borderRadius: 14, padding: '4px 12px', margin: '3px',
                  fontFamily: "'Amiri', serif", fontSize: 15,
                  color: 'var(--navy)', cursor: 'default',
                }}
              >
                {v.word_ar}
              </span>
            ))}
          </div>
          <VocabularyList words={words} variant="panel" />
        </>
      )}
    </div>
  )
}

/** Slide-in window showing one lesson: full screen on mobile, side panel on desktop. */
export default function LessonPanel({ lesson, unitVocab }) {
  const navigate = useNavigate()
  const [tab, setTab]             = useState('text')
  const [dialogues, setDialogues] = useState([])
  const [loading, setLoading]     = useState(false)

  useEffect(() => {
    if (lesson.lesson_type === 'hiwar' || lesson.lesson_type === 'nahw') {
      setLoading(true)
      api.get(`/lessons/${lesson.id}/dialogues`)
        .then(r => setDialogues(r.data))
        .catch(() => setDialogues([]))
        .finally(() => setLoading(false))
    }
  }, [lesson.id])

  // Select best default tab per lesson type
  useEffect(() => {
    if (lesson.lesson_type === 'mufradat') setTab('vocab')
    else if (lesson.lesson_type === 'hiwar') setTab('hiwar')
    else setTab('lessons')
  }, [lesson.id])

  // Words of this lesson; a vocabulary lesson without its own words shows the whole unit
  const lessonVocab = unitVocab.filter(v => v.lesson_id === lesson.id)
  const displayVocab = lessonVocab.length > 0 ? lessonVocab : (lesson.lesson_type === 'mufradat' ? unitVocab : [])

  // Lock background scroll while the panel is open (prevents the page
  // behind from scrolling on mobile and keeps the panel fully visible)
  useEffect(() => {
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => { document.body.style.overflow = prev }
  }, [])

  const leave = () => navigate(`/lessons/${lesson.id}`)

  // Rendered into <body> so no ancestor layout can clip or offset it
  return createPortal(
    <div className="lesson-panel-overlay">
      <div className="lesson-panel-backdrop" onClick={leave} />

      <div className="lesson-panel">
        <PanelHeader lesson={lesson} onBack={leave} />
        <PanelTabs active={tab} onChange={setTab} />

        <div className="lesson-panel-body" style={{ flex: 1, minHeight: 0, overflowY: 'auto', WebkitOverflowScrolling: 'touch', padding: 20 }}>
          {tab === 'lessons' && <LessonTab lesson={lesson} words={displayVocab} dialogues={dialogues} loading={loading} />}
          {tab === 'hiwar'   && <DialogueTab dialogues={dialogues} loading={loading} />}
          {tab === 'vocab'   && <VocabularyTab words={displayVocab} />}
        </div>
      </div>
    </div>,
    document.body
  )
}
