import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../api/client'

function StatCard({ icon, label, value, sub }) {
  return (
    <div style={{
      background: '#fff', borderRadius: 14, padding: '18px 20px',
      border: '1px solid var(--border)', flex: 1, minWidth: 0,
    }}>
      <div style={{ fontSize: 22, marginBottom: 8 }}>{icon}</div>
      <div style={{ fontSize: 22, fontWeight: 700, color: 'var(--navy)', lineHeight: 1 }}>{value ?? '—'}</div>
      <div style={{ fontSize: 11, color: 'var(--muted)', marginTop: 4 }}>{label}</div>
      {sub && <div style={{ fontSize: 10, color: '#bbb', marginTop: 2 }}>{sub}</div>}
    </div>
  )
}

export default function Dashboard() {
  const { student, token }      = useAuth()
  const [units, setUnits]       = useState([])
  const [progress, setProgress] = useState([])
  const [dueCards, setDueCards] = useState(0)
  const [loading, setLoading]   = useState(true)

  useEffect(() => {
    const reqs = [api.get('/units')]
    if (token) {
      reqs.push(api.get('/me/progress'))
      reqs.push(api.get('/me/srs/due'))
    }
    Promise.all(reqs)
      .then(([u, p, s]) => {
        setUnits(u.data)
        if (p) setProgress(p.data)
        if (s) setDueCards(s.data.length)
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [token])

  const completedLessons = progress.filter(p => p.status === 'completed').length
  const totalScore       = progress.reduce((sum, p) => sum + (p.score || 0), 0)

  if (loading) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 260 }}>
      <div style={{ width: 32, height: 32, border: '3px solid var(--border)', borderTopColor: 'var(--gold)', borderRadius: '50%', animation: 'spin .8s linear infinite' }} />
    </div>
  )

  return (
    <div style={{ maxWidth: 1000, margin: '0 auto', padding: '28px 20px' }}>

      {/* Welcome banner */}
      <div style={{
        background: 'var(--navy)', borderRadius: 16, padding: '24px 28px', marginBottom: 24,
        display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16,
      }}>
        <div>
          <div style={{ fontSize: 12, color: 'rgba(255,255,255,.5)', marginBottom: 4 }}>
            أهلاً بك في منصتك التعليمية
          </div>
          <h1 style={{ fontSize: 22, fontWeight: 700, color: '#fff', margin: 0 }}>
            مرحباً،{' '}
            <span style={{ color: 'var(--gold)' }}>
              {student?.name || 'ضيف'}
            </span>
          </h1>
          <p style={{ fontSize: 12, color: 'rgba(255,255,255,.5)', margin: '6px 0 0' }}>
            {token ? 'استمر في رحلتك في تعلم اللغة العربية' : 'سجّل الدخول لتتبع تقدمك وحفظ نتائجك'}
          </p>
        </div>
        <div style={{ fontSize: 48, opacity: .85 }}>📚</div>
      </div>

      {/* Stats row */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 24, flexWrap: 'wrap' }}>
        <StatCard icon="📖" label="الوحدات المتاحة"  value={units.length} />
        <StatCard icon="✅" label="الدروس المكتملة"   value={completedLessons} />
        <StatCard icon="⭐" label="مجموع النقاط"      value={totalScore} />
        <StatCard icon="🗂️" label="بطاقات للمراجعة"  value={dueCards}
          sub={dueCards > 0 ? 'تحتاج مراجعة اليوم' : 'لا توجد بطاقات اليوم'} />
      </div>

      {/* Quick actions */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px,1fr))', gap: 10, marginBottom: 28 }}>
        {[
          { to: '/lessons',   icon: '📖', label: 'الدروس',        desc: 'استكشف الوحدات'   },
          { to: '/exercises', icon: '✏️', label: 'التمارين',      desc: 'تدرب وحسّن مستواك' },
          { to: '/chat',      icon: '🤖', label: 'المساعد الذكي', desc: 'تحدث بالعربية'     },
          { to: '/srs',       icon: '🗂️', label: 'البطاقات',      desc: `${dueCards} بطاقة` },
        ].map(({ to, icon, label, desc }) => (
          <Link
            key={to}
            to={to}
            style={{
              background: '#fff', borderRadius: 12, padding: '16px',
              border: '1px solid var(--border)', textDecoration: 'none',
              display: 'block', transition: 'border-color .15s, box-shadow .15s',
            }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--navy)'; e.currentTarget.style.boxShadow = '0 2px 8px rgba(15,32,68,.1)' }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.boxShadow = 'none' }}
          >
            <div style={{ fontSize: 22, marginBottom: 6 }}>{icon}</div>
            <div style={{ fontWeight: 600, fontSize: 13, color: 'var(--navy)', marginBottom: 2 }}>{label}</div>
            <div style={{ fontSize: 11, color: 'var(--muted)' }}>{desc}</div>
          </Link>
        ))}
      </div>

      {/* Units grid */}
      <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--muted)', letterSpacing: '.06em', marginBottom: 12 }}>
        الوحدات الدراسية
      </div>

      {units.length === 0 ? (
        <div style={{ background: '#fff', borderRadius: 14, padding: '48px 20px', textAlign: 'center', border: '1px solid var(--border)' }}>
          <div style={{ fontSize: 36, marginBottom: 10 }}>📭</div>
          <p style={{ color: 'var(--muted)', fontSize: 13 }}>لا توجد وحدات بعد.</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px,1fr))', gap: 12 }}>
          {units.map(unit => {
            const unitProgress = progress.filter(p => p.unit_id === unit.id)
            const done = unitProgress.filter(p => p.status === 'completed').length
            const pct  = unit.total_lessons > 0 ? Math.round((done / unit.total_lessons) * 100) : 0
            return (
              <Link
                key={unit.id}
                to="/lessons"
                state={{ unitId: unit.id }}
                style={{
                  background: '#fff', borderRadius: 14, padding: '18px 20px',
                  border: '1px solid var(--border)', textDecoration: 'none',
                  display: 'block', transition: 'border-color .15s',
                }}
                onMouseEnter={e => e.currentTarget.style.borderColor = 'var(--navy)'}
                onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border)'}
              >
                <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: 10 }}>
                  <div style={{
                    width: 32, height: 32, borderRadius: 9,
                    background: 'var(--navy)', color: 'var(--gold)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: 12, fontWeight: 700,
                  }}>
                    {unit.unit_number}
                  </div>
                  <span style={{
                    fontSize: 10, color: 'var(--muted)', background: 'var(--cream)',
                    border: '1px solid var(--border)', borderRadius: 6, padding: '2px 7px',
                  }}>
                    {unit.total_lessons} درس
                  </span>
                </div>
                <div style={{ fontFamily: "'Amiri', serif", fontSize: 16, color: 'var(--navy)', marginBottom: 2 }}>
                  {unit.title_ar}
                </div>
                <div style={{ fontSize: 11, color: 'var(--muted)', marginBottom: 12 }}>{unit.title_tr}</div>
                <div style={{ height: 3, background: 'var(--border)', borderRadius: 2, overflow: 'hidden' }}>
                  <div style={{ height: '100%', background: 'var(--gold)', borderRadius: 2, width: `${pct}%`, transition: 'width .4s' }} />
                </div>
                <div style={{ fontSize: 10, color: 'var(--muted)', marginTop: 4 }}>{pct}% مكتمل</div>
              </Link>
            )
          })}
        </div>
      )}
    </div>
  )
}
