import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/client'
import { useAuth } from '../context/AuthContext'

// 4 rating buttons mapped to SM-2 quality scores
const RATINGS = [
  { q: 1, label: 'صعب',       sub: '× 1 يوم',  bg: '#fef2f2', color: '#dc2626', border: '#fecaca' },
  { q: 3, label: 'متوسط',     sub: '× 3 أيام', bg: '#fff7ed', color: '#d97706', border: '#fed7aa' },
  { q: 4, label: 'سهل',       sub: '× 7 أيام', bg: '#f0fdf4', color: '#16a34a', border: '#bbf7d0' },
  { q: 5, label: 'سهل جداً',  sub: '× 14 يوم', bg: '#eff6ff', color: '#2563eb', border: '#bfdbfe' },
]

export default function SRSFlashcards() {
  const { token }                   = useAuth()
  const [cards, setCards]           = useState([])
  const [current, setCurrent]       = useState(0)
  const [flipped, setFlipped]       = useState(false)
  const [loading, setLoading]       = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [done, setDone]             = useState(false)
  const [stats, setStats]           = useState({ reviewed: 0, easy: 0, hard: 0 })

  useEffect(() => { if (token) fetchCards(); else setLoading(false) }, [token])

  const fetchCards = () => {
    setLoading(true)
    api.get('/me/srs/due')
      .then(r => {
        setCards(r.data)
        setCurrent(0); setFlipped(false); setDone(false)
        setStats({ reviewed: 0, easy: 0, hard: 0 })
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }

  const handleReview = async (quality) => {
    if (submitting) return
    setSubmitting(true)
    const card = cards[current]
    try {
      await api.post('/me/srs/review', { vocabulary_id: card.vocabulary_id, quality })
      setStats(s => ({
        reviewed: s.reviewed + 1,
        easy:  s.easy  + (quality >= 4 ? 1 : 0),
        hard:  s.hard  + (quality <= 2 ? 1 : 0),
      }))
      if (current + 1 >= cards.length) setDone(true)
      else { setCurrent(c => c + 1); setFlipped(false) }
    } catch (e) { console.error(e) }
    finally { setSubmitting(false) }
  }

  // ── Guest wall ──
  if (!token) return (
    <div style={{ maxWidth: 400, margin: '80px auto', padding: '0 16px', textAlign: 'center' }}>
      <div style={{ fontSize: 52, marginBottom: 14 }}>🗂️</div>
      <h2 style={{ fontFamily: "'Amiri', serif", fontSize: 20, color: 'var(--navy)', marginBottom: 8 }}>
        بطاقات الحفظ الذكية
      </h2>
      <p style={{ fontSize: 13, color: 'var(--muted)', marginBottom: 24, lineHeight: 1.6 }}>
        سجّل الدخول لتتمكن من مراجعة المفردات بنظام التكرار المتباعد (SRS).
      </p>
      <Link to="/login" style={{
        display: 'inline-block', background: 'var(--navy)', color: '#fff',
        borderRadius: 10, padding: '11px 32px', fontWeight: 600, textDecoration: 'none', fontSize: 14,
      }}>
        تسجيل الدخول
      </Link>
    </div>
  )

  // ── Loading ──
  if (loading) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 300 }}>
      <div style={{ width: 32, height: 32, border: '3px solid var(--border)', borderTopColor: 'var(--gold)', borderRadius: '50%', animation: 'spin .8s linear infinite' }} />
    </div>
  )

  // ── No cards ──
  if (!loading && cards.length === 0) return (
    <div style={{ maxWidth: 420, margin: '60px auto', padding: '0 16px', textAlign: 'center' }}>
      <div style={{ fontSize: 56, marginBottom: 16 }}>🎉</div>
      <h2 style={{ fontFamily: "'Amiri', serif", fontSize: 22, color: 'var(--navy)', marginBottom: 8 }}>
        أحسنت! لا توجد بطاقات للمراجعة اليوم
      </h2>
      <p style={{ color: 'var(--muted)', marginBottom: 24, fontSize: 13 }}>
        عد غداً للمراجعة، أو أضف وحدة جديدة من صفحة الدروس.
      </p>
      <Link to="/lessons" style={{
        display: 'inline-block', background: 'var(--navy)', color: '#fff',
        borderRadius: 9, padding: '10px 28px', fontWeight: 500, textDecoration: 'none', fontSize: 13,
      }}>
        اذهب إلى الدروس
      </Link>
    </div>
  )

  // ── Done screen ──
  if (done) {
    const pct = stats.reviewed > 0 ? Math.round((stats.easy / stats.reviewed) * 100) : 0
    return (
      <div style={{ maxWidth: 420, margin: '40px auto', padding: '0 16px', textAlign: 'center' }}>
        <div style={{ fontSize: 52, marginBottom: 12 }}>
          {pct >= 70 ? '🏆' : pct >= 40 ? '👏' : '💪'}
        </div>
        <h2 style={{ fontFamily: "'Amiri', serif", fontSize: 22, color: 'var(--navy)', marginBottom: 20 }}>
          انتهت جلسة المراجعة
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 10, marginBottom: 28 }}>
          {[
            ['📚', stats.reviewed, 'بطاقة'],
            ['✅', stats.easy,    'سهلة'],
            ['📊', `${pct}%`,    'نجاح'],
          ].map(([icon, val, label]) => (
            <div key={label} style={{
              background: '#fff', border: '1px solid var(--border)', borderRadius: 10, padding: '14px 8px',
            }}>
              <div style={{ fontSize: 22, marginBottom: 4 }}>{icon}</div>
              <div style={{ fontSize: 20, fontWeight: 700, color: 'var(--navy)', fontFamily: "'Amiri', serif" }}>{val}</div>
              <div style={{ fontSize: 11, color: 'var(--muted)' }}>{label}</div>
            </div>
          ))}
        </div>
        <button
          onClick={fetchCards}
          style={{
            background: 'var(--navy)', color: '#fff', border: 'none', cursor: 'pointer',
            borderRadius: 9, padding: '10px 28px', fontWeight: 500, fontSize: 13,
            fontFamily: 'DM Sans, sans-serif',
          }}
        >
          مراجعة مجدداً
        </button>
      </div>
    )
  }

  const card     = cards[current]
  const progress = Math.round((current / cards.length) * 100)

  return (
    <div style={{ maxWidth: 480, margin: '32px auto', padding: '0 16px' }}>

      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h1 style={{ fontFamily: "'Amiri', serif", fontSize: 20, color: 'var(--navy)' }}>
          بطاقات المراجعة
        </h1>
        <span style={{
          background: '#fff', border: '1px solid var(--border)', borderRadius: 8,
          padding: '4px 12px', fontSize: 12, color: 'var(--muted)',
        }}>
          {current + 1} / {cards.length}
        </span>
      </div>

      {/* Progress bar */}
      <div style={{ height: 4, background: 'var(--border)', borderRadius: 2, marginBottom: 28, overflow: 'hidden' }}>
        <div style={{ height: '100%', background: 'var(--gold)', borderRadius: 2, width: `${progress}%`, transition: 'width .5s' }} />
      </div>

      {/* Flashcard */}
      <div
        className="card-flip"
        style={{ cursor: 'pointer', marginBottom: 24 }}
        onClick={() => !submitting && setFlipped(f => !f)}
      >
        <div className={`card-inner${flipped ? ' flipped' : ''}`} style={{ height: 240 }}>

          {/* Front — Arabic word */}
          <div className="card-face" style={{
            position: 'absolute', inset: 0,
            background: 'var(--navy)',
            borderRadius: 16,
            display: 'flex', flexDirection: 'column',
            alignItems: 'center', justifyContent: 'center',
            padding: 32, textAlign: 'center',
          }}>
            <div style={{ fontSize: 10, color: 'rgba(201,168,76,.7)', letterSpacing: '.1em', marginBottom: 16 }}>
              الكلمة العربية
            </div>
            <div style={{
              fontFamily: "'Amiri', serif", fontSize: 48, color: '#fff',
              lineHeight: 1.2, marginBottom: 12,
            }}>
              {card.word_ar}
            </div>
            {!flipped && (
              <div style={{ fontSize: 11, color: 'rgba(255,255,255,.4)', marginTop: 8 }}>
                اضغط لرؤية الترجمة
              </div>
            )}
          </div>

          {/* Back — Turkish + example */}
          <div className="card-face card-back" style={{
            position: 'absolute', inset: 0,
            background: '#fff', border: '1px solid var(--border)',
            borderRadius: 16,
            display: 'flex', flexDirection: 'column',
            alignItems: 'center', justifyContent: 'center',
            padding: 28, textAlign: 'center',
          }}>
            <div style={{ fontSize: 10, color: 'var(--muted)', letterSpacing: '.1em', marginBottom: 12 }}>
              الترجمة — Çeviri
            </div>
            <div style={{ fontSize: 26, fontWeight: 600, color: 'var(--navy)', marginBottom: 16 }} dir="ltr">
              {card.translation_tr}
            </div>
            {card.example_ar && (
              <div style={{
                background: 'var(--cream)', border: '1px solid var(--border)',
                borderRadius: 10, padding: '10px 16px',
                fontFamily: "'Amiri', serif", fontSize: 15, color: 'var(--text)',
                direction: 'rtl', lineHeight: 1.7,
              }}>
                {card.example_ar}
              </div>
            )}
          </div>

        </div>
      </div>

      {/* Action buttons */}
      {!flipped ? (
        <div style={{ textAlign: 'center' }}>
          <button
            onClick={() => setFlipped(true)}
            style={{
              background: '#fff', border: '1px solid var(--border)',
              borderRadius: 9, padding: '10px 32px',
              color: 'var(--navy)', fontWeight: 500, fontSize: 13,
              cursor: 'pointer', fontFamily: 'DM Sans, sans-serif',
              boxShadow: '0 1px 3px rgba(0,0,0,.06)',
            }}
          >
            عرض الترجمة
          </button>
        </div>
      ) : (
        <div>
          <div style={{ textAlign: 'center', fontSize: 11, color: 'var(--muted)', marginBottom: 10 }}>
            كيف كانت إجابتك؟
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: 8 }}>
            {RATINGS.map(({ q, label, sub, bg, color, border }) => (
              <button
                key={q}
                onClick={() => handleReview(q)}
                disabled={submitting}
                style={{
                  background: bg, border: `1px solid ${border}`, borderRadius: 10,
                  padding: '12px 6px', cursor: submitting ? 'not-allowed' : 'pointer',
                  opacity: submitting ? .6 : 1, transition: 'all .15s',
                  fontFamily: 'DM Sans, sans-serif',
                }}
              >
                <div style={{ fontSize: 13, fontWeight: 700, color, marginBottom: 3 }}>{label}</div>
                <div style={{ fontSize: 10, color: 'var(--muted)' }}>{sub}</div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
