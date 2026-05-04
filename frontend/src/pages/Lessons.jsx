import { useEffect, useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../api/client'
import { useAuth } from '../context/AuthContext'

const TYPE_LABEL = {
  hiwar: 'حوار', mufradat: 'مفردات', nahw: 'نحو',
  tadrib: 'تدريب', aswat: 'أصوات',
}
const TYPE_DOT = {
  hiwar:    '#185FA5',
  mufradat: '#1D9E75',
  nahw:     '#3C3489',
  tadrib:   '#854F0B',
  aswat:    '#712B13',
}

/* ── Lesson detail panel with 3 tabs ──────────────────────────── */
function LessonPanel({ lesson, unitVocab, onClose }) {
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

  const lessonVocab = unitVocab.filter(v => v.lesson_id === lesson.id)
  const displayVocab = lessonVocab.length > 0 ? lessonVocab : (lesson.lesson_type === 'mufradat' ? unitVocab : [])
  const dotColor = TYPE_DOT[lesson.lesson_type] || '#6b7280'

  const TABS = [
    { key: 'lessons', label: 'الدروس' },
    { key: 'hiwar',   label: 'الحوار' },
    { key: 'vocab',   label: 'المفردات' },
  ]

  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 200, display: 'flex', direction: 'rtl' }}>
      {/* Backdrop */}
      <div
        onClick={() => navigate(`/lessons/${lesson.id}`)}
        style={{ position: 'absolute', inset: 0, background: 'rgba(15,32,68,.5)', backdropFilter: 'blur(3px)' }}
      />

      {/* Panel — slides in from right */}
      <div style={{
        position: 'relative', marginRight: 'auto',
        width: '100%', maxWidth: 540,
        background: '#fff', borderLeft: '1px solid var(--border)',
        height: '100%', display: 'flex', flexDirection: 'column',
        boxShadow: '-8px 0 32px rgba(15,32,68,.12)',
        animation: 'slideUp .25s ease-out',
      }}>

        {/* Panel header */}
        <div style={{
          padding: '12px 20px 14px', borderBottom: '1px solid var(--border)',
          background: 'var(--navy)',
        }}>
          {/* Back button row */}
          <button
            onClick={() => navigate(`/lessons/${lesson.id}`)}
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
                  borderRadius: '50%', background: dotColor, flexShrink: 0,
                }} />
                <span style={{ fontSize: 11, color: 'rgba(255,255,255,.5)', letterSpacing: '.05em' }}>
                  {TYPE_LABEL[lesson.lesson_type] || lesson.lesson_type} · درس {lesson.lesson_number}
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
              onClick={() => navigate(`/lessons/${lesson.id}`)}
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

        {/* Tabs */}
        <div style={{
          display: 'flex', borderBottom: '1px solid var(--border)',
          background: '#fff', padding: '0 20px', gap: 4,
        }}>
          {TABS.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setTab(key)}
              className={tab === key ? 'tab-active' : 'tab-inactive'}
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

        {/* Tab content */}
        <div style={{ flex: 1, overflowY: 'auto', padding: 20 }}>

          {/* ── الدروس tab ───────────────────────────────── */}
          {tab === 'lessons' && (
            <div>
              {/* Grammar focus box for nahw/grammar lessons */}
              {lesson.grammar_focus && (
                <div style={{ marginBottom: 20 }}>
                  <div style={{ fontSize: 10, color: 'var(--muted)', letterSpacing: '.08em', marginBottom: 12, fontWeight: 500 }}>
                    القواعد النحوية — GRAMMAR
                  </div>
                  {lesson.grammar_focus.split('|').map((rule, i) => (
                    <div key={i} style={{
                      background: '#f5f3ff', border: '1px solid #ddd6fe',
                      borderRadius: 10, padding: '12px 16px', marginBottom: 8,
                      display: 'flex', gap: 12, alignItems: 'flex-start',
                    }}>
                      <div style={{
                        width: 22, height: 22, borderRadius: '50%', flexShrink: 0,
                        background: '#7c3aed', color: '#fff',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: 10, fontWeight: 700,
                      }}>
                        {i + 1}
                      </div>
                      <div style={{ fontFamily: "'Amiri', serif", fontSize: 16, color: '#4c1d95', lineHeight: 1.6, direction: 'rtl' }}>
                        {rule.trim()}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {lesson.lesson_type === 'mufradat' && displayVocab.length > 0 && (
                <>
                  <div style={{ fontSize: 10, color: 'var(--muted)', letterSpacing: '.08em', marginBottom: 12, fontWeight: 500 }}>
                    المفردات — VOCABULARY
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                    {displayVocab.map(v => (
                      <div key={v.id} style={{
                        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                        padding: '10px 14px',
                        background: 'var(--cream)', border: '1px solid var(--border)', borderRadius: 10,
                      }}>
                        <div>
                          <span style={{ fontFamily: "'Amiri', serif", fontSize: 18, color: 'var(--navy)' }}>
                            {v.word_ar}
                          </span>
                          {v.word_type && (
                            <span style={{
                              marginRight: 8, fontSize: 10, color: 'var(--muted)',
                              background: 'var(--cream2)', border: '1px solid var(--border)',
                              borderRadius: 4, padding: '1px 6px',
                            }}>
                              {v.word_type}
                            </span>
                          )}
                          {v.example_ar && (
                            <div style={{ fontSize: 12, color: 'var(--muted)', marginTop: 3, fontFamily: "'Amiri', serif" }}>
                              {v.example_ar}
                            </div>
                          )}
                        </div>
                        <span style={{ fontSize: 12, color: 'var(--navy)', fontWeight: 500, flexShrink: 0, marginRight: 10 }} dir="ltr">
                          {v.translation_tr}
                        </span>
                      </div>
                    ))}
                  </div>
                </>
              )}

              {(lesson.lesson_type === 'hiwar') && (
                loading ? (
                  <div style={{ display: 'flex', justifyContent: 'center', padding: 40 }}>
                    <div style={{ width: 24, height: 24, border: '2px solid var(--border)', borderTopColor: 'var(--gold)', borderRadius: '50%', animation: 'spin .8s linear infinite' }} />
                  </div>
                ) : dialogues.length === 0 ? (
                  <p style={{ color: 'var(--muted)', textAlign: 'center', padding: '40px 0', fontSize: 13 }}>
                    لا يوجد نص لهذا الحوار بعد
                  </p>
                ) : dialogues.map(dialogue => (
                  <div key={dialogue.id} style={{ marginBottom: 24 }}>
                    {dialogue.title_ar && (
                      <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--navy)', marginBottom: 4 }}>
                        {dialogue.title_ar}
                      </div>
                    )}
                    {dialogue.situation_tr && (
                      <div style={{ fontSize: 11, color: 'var(--muted)', fontStyle: 'italic', marginBottom: 12 }} dir="ltr">
                        {dialogue.situation_tr}
                      </div>
                    )}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                      {dialogue.lines?.map((line, i) => (
                        <div key={i} style={{
                          display: 'flex', gap: 10, alignItems: 'flex-start',
                          opacity: line.is_key_phrase ? 1 : 0.65,
                        }}>
                          <span style={{
                            fontSize: 11, fontWeight: 600, color: 'var(--gold)',
                            minWidth: 80, flexShrink: 0, paddingTop: 2, fontFamily: "'Amiri', serif",
                          }}>
                            {line.speaker}
                          </span>
                          <div style={{ flex: 1 }}>
                            <div style={{
                              fontFamily: "'Amiri', serif", fontSize: 16,
                              color: line.is_key_phrase ? 'var(--navy)' : 'var(--text)',
                              fontWeight: line.is_key_phrase ? 700 : 400,
                              lineHeight: 1.6,
                            }}>
                              {line.text_ar}
                            </div>
                            {line.translation_tr && (
                              <div style={{ fontSize: 11, color: 'var(--muted)', marginTop: 2 }} dir="ltr">
                                {line.translation_tr}
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))
              )}

              {(lesson.lesson_type === 'tadrib' || lesson.lesson_type === 'aswat') && (
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

              {lesson.lesson_type === 'nahw' && !lesson.grammar_focus && (
                <p style={{ color: 'var(--muted)', textAlign: 'center', padding: '40px 0', fontSize: 13 }}>
                  لا توجد قواعد نحوية مدخلة لهذا الدرس بعد
                </p>
              )}
            </div>
          )}

          {/* ── الحوار tab ────────────────────────────────── */}
          {tab === 'hiwar' && (
            <div>
              {loading ? (
                <div style={{ display: 'flex', justifyContent: 'center', padding: 40 }}>
                  <div style={{ width: 24, height: 24, border: '2px solid var(--border)', borderTopColor: 'var(--gold)', borderRadius: '50%', animation: 'spin .8s linear infinite' }} />
                </div>
              ) : dialogues.length === 0 ? (
                <p style={{ color: 'var(--muted)', textAlign: 'center', padding: '40px 0', fontSize: 13 }}>
                  لا يوجد حوار لهذا الدرس
                </p>
              ) : dialogues.map(dialogue => (
                <div key={dialogue.id} style={{ marginBottom: 28 }}>
                  {dialogue.title_ar && (
                    <div style={{
                      fontSize: 14, fontWeight: 600, color: 'var(--navy)',
                      fontFamily: "'Amiri', serif", marginBottom: 6,
                    }}>
                      {dialogue.title_ar}
                    </div>
                  )}
                  {dialogue.situation_tr && (
                    <div style={{
                      fontSize: 11, color: 'var(--muted)', fontStyle: 'italic',
                      marginBottom: 14, padding: '6px 12px',
                      background: 'var(--cream)', border: '1px solid var(--border)',
                      borderRadius: 8,
                    }} dir="ltr">
                      📍 {dialogue.situation_tr}
                    </div>
                  )}

                  {/* Dialogue bubbles */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    {dialogue.lines?.map((line, i) => {
                      const isRight = i % 2 === 0
                      return (
                        <div key={i} style={{
                          display: 'flex', flexDirection: isRight ? 'row' : 'row-reverse',
                          alignItems: 'flex-end', gap: 8,
                        }}>
                          <div style={{
                            width: 30, height: 30, borderRadius: '50%', flexShrink: 0,
                            background: isRight ? 'var(--navy)' : '#185FA5',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            fontSize: 11, fontWeight: 700, color: '#fff',
                            fontFamily: "'Amiri', serif",
                          }}>
                            {line.speaker?.[0] || '؟'}
                          </div>
                          <div style={{
                            background: isRight ? 'var(--cream)' : 'var(--navy)',
                            border: `1px solid ${isRight ? 'var(--border)' : 'var(--navy)'}`,
                            borderRadius: isRight ? '4px 12px 12px 12px' : '12px 4px 12px 12px',
                            padding: '10px 14px', maxWidth: '75%',
                          }}>
                            <div style={{
                              fontFamily: "'Amiri', serif", fontSize: 15,
                              color: isRight ? 'var(--navy)' : '#fff',
                              lineHeight: 1.6, direction: 'rtl',
                              fontWeight: line.is_key_phrase ? 700 : 400,
                            }}>
                              {line.text_ar}
                            </div>
                            {line.translation_tr && (
                              <div style={{ fontSize: 11, color: isRight ? 'var(--muted)' : 'rgba(255,255,255,.55)', marginTop: 3 }} dir="ltr">
                                {line.translation_tr}
                              </div>
                            )}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* ── المفردات tab ─────────────────────────────── */}
          {tab === 'vocab' && (
            <div>
              <div style={{ fontSize: 10, color: 'var(--muted)', letterSpacing: '.08em', marginBottom: 14, fontWeight: 500 }}>
                مفردات الوحدة — VOCABULARY
              </div>
              {displayVocab.length === 0 ? (
                <p style={{ color: 'var(--muted)', textAlign: 'center', padding: '40px 0', fontSize: 13 }}>
                  لا توجد مفردات مرتبطة بهذا الدرس
                </p>
              ) : (
                <>
                  {/* Chips row */}
                  <div style={{ display: 'flex', flexWrap: 'wrap', marginBottom: 18 }}>
                    {displayVocab.map(v => (
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
                  {/* Full list */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                    {displayVocab.map(v => (
                      <div key={v.id} style={{
                        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                        padding: '10px 14px',
                        background: 'var(--cream)', border: '1px solid var(--border)', borderRadius: 10,
                      }}>
                        <div>
                          <span style={{ fontFamily: "'Amiri', serif", fontSize: 18, color: 'var(--navy)' }}>
                            {v.word_ar}
                          </span>
                          {v.word_type && (
                            <span style={{
                              marginRight: 8, fontSize: 10, color: 'var(--muted)',
                              background: '#fff', border: '1px solid var(--border)',
                              borderRadius: 4, padding: '1px 6px',
                            }}>
                              {v.word_type}
                            </span>
                          )}
                          {v.example_ar && (
                            <div style={{ fontSize: 12, color: 'var(--muted)', marginTop: 3, fontFamily: "'Amiri', serif" }}>
                              {v.example_ar}
                            </div>
                          )}
                        </div>
                        <div style={{ textAlign: 'left', flexShrink: 0, marginRight: 12 }}>
                          <div style={{ fontSize: 13, fontWeight: 500, color: 'var(--navy)' }} dir="ltr">
                            {v.translation_tr}
                          </div>
                          {v.translation_en && (
                            <div style={{ fontSize: 11, color: 'var(--muted)' }} dir="ltr">{v.translation_en}</div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}


/* ── Main Lessons page ──────────────────────────────────────────── */
export default function Lessons() {
  const { token }                           = useAuth()
  const [units, setUnits]                   = useState([])
  const [selectedUnit, setSelectedUnit]     = useState(null)
  const [lessons, setLessons]               = useState([])
  const [vocab, setVocab]                   = useState([])
  const [tab, setTab]                       = useState('lessons')
  const [srsMsg, setSrsMsg]                 = useState('')
  const [loadingUnits, setLoadingUnits]     = useState(true)
  const [loadingContent, setLoadingContent] = useState(false)
  const [openLesson, setOpenLesson]         = useState(null)

  useEffect(() => {
    api.get('/units').then(r => {
      setUnits(r.data)
      if (r.data[0]) setSelectedUnit(r.data[0])
    }).finally(() => setLoadingUnits(false))
  }, [])

  useEffect(() => {
    if (!selectedUnit) return
    setLoadingContent(true)
    setSrsMsg('')
    Promise.all([
      api.get(`/units/${selectedUnit.id}/lessons`),
      api.get(`/units/${selectedUnit.id}/vocabulary`),
    ]).then(([l, v]) => {
      setLessons(l.data)
      setVocab(v.data)
    }).finally(() => setLoadingContent(false))
  }, [selectedUnit])

  const addToSRS = async () => {
    try {
      const res = await api.post(`/me/srs/add-unit/${selectedUnit.id}`)
      setSrsMsg(`تمت إضافة ${res.data.added} بطاقة جديدة`)
    } catch { setSrsMsg('حدث خطأ') }
  }

  if (loadingUnits) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 260 }}>
      <div style={{ width: 32, height: 32, border: '3px solid var(--border)', borderTopColor: 'var(--gold)', borderRadius: '50%', animation: 'spin .8s linear infinite' }} />
    </div>
  )

  return (
    <div style={{ maxWidth: 1100, margin: '0 auto', padding: '28px 20px' }}>

      {/* Lesson panel overlay */}
      {openLesson && (
        <LessonPanel
          lesson={openLesson}
          unitVocab={vocab}
          onClose={() => setOpenLesson(null)}
        />
      )}

      <div style={{ display: 'flex', gap: 20 }}>

        {/* Units sidebar */}
        <aside style={{ width: 200, flexShrink: 0 }}>
          <div style={{ fontSize: 9, letterSpacing: '.1em', color: 'var(--muted)', fontWeight: 500, marginBottom: 10 }}>
            الوحدات الدراسية
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            {units.map(unit => {
              const isActive = selectedUnit?.id === unit.id
              return (
                <button
                  key={unit.id}
                  onClick={() => setSelectedUnit(unit)}
                  style={{
                    width: '100%', textAlign: 'right', padding: '10px 14px',
                    borderRadius: 10, cursor: 'pointer', border: 'none', transition: 'all .15s',
                    background: isActive ? 'var(--navy)' : '#fff',
                    borderRight: isActive ? '3px solid var(--gold)' : '3px solid transparent',
                    boxShadow: isActive ? 'none' : '0 1px 3px rgba(0,0,0,.05)',
                    fontFamily: 'DM Sans, sans-serif',
                  }}
                >
                  <div style={{
                    fontFamily: "'Amiri', serif", fontSize: 14,
                    color: isActive ? '#fff' : 'var(--navy)',
                    lineHeight: 1.3,
                  }}>
                    {unit.title_ar}
                  </div>
                  <div style={{ fontSize: 10, color: isActive ? 'rgba(255,255,255,.55)' : 'var(--muted)', marginTop: 2 }}>
                    {unit.total_lessons} درس
                  </div>
                </button>
              )
            })}
          </div>
        </aside>

        {/* Main content */}
        <div style={{ flex: 1, minWidth: 0 }}>
          {selectedUnit ? (
            <>
              {/* Unit header */}
              <div style={{
                background: 'var(--navy)', borderRadius: 14,
                padding: '18px 22px', marginBottom: 20,
                display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between',
              }}>
                <div>
                  <div style={{ fontSize: 10, color: 'rgba(201,168,76,.7)', letterSpacing: '.06em', marginBottom: 4 }}>
                    الوحدة {selectedUnit.unit_number}
                  </div>
                  <div style={{ fontFamily: "'Amiri', serif", fontSize: 20, color: '#fff', marginBottom: 2 }}>
                    {selectedUnit.title_ar}
                  </div>
                  <div style={{ fontSize: 11, color: 'rgba(255,255,255,.45)' }}>{selectedUnit.title_tr}</div>
                  {srsMsg && (
                    <div style={{ marginTop: 8, fontSize: 11, color: '#C9A84C', background: 'rgba(201,168,76,.1)', borderRadius: 6, padding: '4px 10px', display: 'inline-block' }}>
                      {srsMsg}
                    </div>
                  )}
                </div>
                {token ? (
                  <button
                    onClick={addToSRS}
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

              {/* Tabs */}
              <div style={{ display: 'flex', gap: 0, borderBottom: '1px solid var(--border)', marginBottom: 20 }}>
                {[['lessons','الدروس'], ['vocab','المفردات']].map(([key, label]) => (
                  <button
                    key={key}
                    onClick={() => setTab(key)}
                    className={tab === key ? 'tab-active' : 'tab-inactive'}
                    style={{
                      padding: '10px 18px', fontSize: 13, fontWeight: 500,
                      background: 'none', border: 'none', borderBottom: tab === key ? '2px solid var(--gold)' : '2px solid transparent',
                      cursor: 'pointer', fontFamily: 'DM Sans, sans-serif', transition: 'all .15s',
                      color: tab === key ? 'var(--navy)' : 'var(--muted)',
                    }}
                  >
                    {label}
                  </button>
                ))}
              </div>

              {loadingContent ? (
                <div style={{ display: 'flex', justifyContent: 'center', padding: 40 }}>
                  <div style={{ width: 28, height: 28, border: '3px solid var(--border)', borderTopColor: 'var(--gold)', borderRadius: '50%', animation: 'spin .8s linear infinite' }} />
                </div>
              ) : tab === 'lessons' ? (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 12 }}>
                  {lessons.map(lesson => {
                    const dotColor = TYPE_DOT[lesson.lesson_type] || '#6b7280'
                    return (
                      <button
                        key={lesson.id}
                        onClick={() => setOpenLesson(lesson)}
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
                              {TYPE_LABEL[lesson.lesson_type] || lesson.lesson_type}
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
                  })}
                </div>
              ) : (
                /* Vocabulary tab */
                <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                  {vocab.map(v => (
                    <div key={v.id} style={{
                      background: '#fff', border: '1px solid var(--border)', borderRadius: 10,
                      padding: '11px 16px',
                      display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12,
                    }}>
                      <div>
                        <span style={{ fontFamily: "'Amiri', serif", fontSize: 19, color: 'var(--navy)' }}>
                          {v.word_ar}
                        </span>
                        {v.word_type && (
                          <span style={{
                            marginRight: 8, fontSize: 10, color: 'var(--muted)',
                            background: 'var(--cream)', border: '1px solid var(--border)',
                            borderRadius: 4, padding: '1px 6px',
                          }}>
                            {v.word_type}
                          </span>
                        )}
                        {v.example_ar && (
                          <div style={{ fontSize: 12, color: 'var(--muted)', marginTop: 2, fontFamily: "'Amiri', serif" }}>
                            {v.example_ar}
                          </div>
                        )}
                      </div>
                      <div style={{ textAlign: 'left', flexShrink: 0 }}>
                        <div style={{ fontSize: 13, fontWeight: 500, color: 'var(--navy)' }} dir="ltr">
                          {v.translation_tr}
                        </div>
                        {v.translation_en && (
                          <div style={{ fontSize: 11, color: 'var(--muted)' }} dir="ltr">{v.translation_en}</div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </>
          ) : (
            <div style={{ textAlign: 'center', color: 'var(--muted)', padding: '60px 0' }}>
              اختر وحدة من القائمة
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

