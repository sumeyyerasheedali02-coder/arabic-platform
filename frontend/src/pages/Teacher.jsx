import { useState, useEffect } from 'react'
import api from '../api/client'

export default function Teacher() {
  const [students, setStudents]   = useState([])
  const [unitStats, setUnitStats] = useState([])
  const [loading, setLoading]     = useState(true)
  const [error, setError]         = useState(null)

  useEffect(() => {
    Promise.all([
      api.get('/teacher/students'),
      api.get('/teacher/units/stats'),
    ])
      .then(([sRes, uRes]) => {
        setStudents(sRes.data)
        setUnitStats(uRes.data)
      })
      .catch(err => setError(
        err.response?.status === 401 || err.response?.status === 403
          ? 'هذه الصفحة مخصصة للمعلمين فقط.'
          : 'فشل تحميل البيانات. تأكد من تشغيل الخادم.'
      ))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 280 }}>
      <div style={{ width: 32, height: 32, border: '3px solid var(--border)', borderTopColor: 'var(--gold)', borderRadius: '50%', animation: 'spin .8s linear infinite' }} />
    </div>
  )

  if (error) return (
    <div style={{ maxWidth: 480, margin: '80px auto', textAlign: 'center', padding: '0 20px' }}>
      <div style={{ fontSize: 48, marginBottom: 12 }}>🔒</div>
      <p style={{ color: 'var(--muted)', fontSize: 14 }}>{error}</p>
    </div>
  )

  const totalStudents  = students.length
  const avgScore       = totalStudents
    ? Math.round(students.reduce((s, x) => s + (x.total_score || 0), 0) / totalStudents)
    : 0
  const totalLessons   = students.reduce((s, x) => s + (x.lessons_done || 0), 0)

  return (
    <div style={{ maxWidth: 1000, margin: '0 auto', padding: '28px 20px' }}>

      {/* Page header */}
      <div style={{ marginBottom: 28 }}>
        <div style={{ fontFamily: "'Amiri', serif", fontSize: 22, color: 'var(--navy)', marginBottom: 4 }}>
          لوحة تحكم المعلم
        </div>
        <div style={{ fontSize: 12, color: 'var(--muted)' }}>
          إحصائيات الطلاب وتقدمهم في تعلم اللغة العربية
        </div>
      </div>

      {/* Summary cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12, marginBottom: 28 }}>
        {[
          { label: 'إجمالي الطلاب',  value: totalStudents, icon: '👥' },
          { label: 'متوسط النقاط',   value: avgScore,       icon: '⭐' },
          { label: 'دروس مكتملة',    value: totalLessons,   icon: '✅' },
        ].map(({ label, value, icon }) => (
          <div key={label} style={{
            background: '#fff', border: '1px solid var(--border)', borderRadius: 12,
            padding: '18px 20px', display: 'flex', alignItems: 'center', gap: 14,
          }}>
            <div style={{
              width: 42, height: 42, borderRadius: 10, background: 'var(--cream)',
              display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 20, flexShrink: 0,
            }}>
              {icon}
            </div>
            <div>
              <div style={{ fontSize: 22, fontWeight: 700, color: 'var(--navy)', fontFamily: "'Amiri', serif" }}>
                {value}
              </div>
              <div style={{ fontSize: 11, color: 'var(--muted)' }}>{label}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Unit stats */}
      {unitStats.length > 0 && (
        <div style={{ marginBottom: 28 }}>
          <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--navy)', marginBottom: 12 }}>
            إحصائيات الوحدات
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: 10 }}>
            {unitStats.map(u => (
              <div key={u.unit_number} style={{
                background: '#fff', border: '1px solid var(--border)', borderRadius: 12, padding: '16px 18px',
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                  <div style={{ fontFamily: "'Amiri', serif", fontSize: 15, color: 'var(--navy)' }}>
                    {u.title_ar}
                  </div>
                  <span style={{
                    fontSize: 10, color: 'var(--muted)',
                    background: 'var(--cream)', border: '1px solid var(--border)',
                    borderRadius: 6, padding: '2px 7px',
                  }}>
                    {u.unit_number}
                  </span>
                </div>
                <div style={{ marginBottom: 6 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: 'var(--muted)', marginBottom: 4 }}>
                    <span>نسبة الإتمام</span>
                    <span style={{ color: 'var(--navy)', fontWeight: 600 }}>
                      {Math.round(u.completion_pct || 0)}%
                    </span>
                  </div>
                  <div style={{ height: 5, background: 'var(--border)', borderRadius: 3, overflow: 'hidden' }}>
                    <div style={{
                      height: '100%', background: 'var(--gold)', borderRadius: 3,
                      width: `${Math.min(100, u.completion_pct || 0)}%`, transition: 'width .4s',
                    }} />
                  </div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11 }}>
                  <span style={{ color: 'var(--muted)' }}>متوسط النقاط</span>
                  <span style={{ color: '#1D9E75', fontWeight: 600 }}>{Math.round(u.avg_score || 0)}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Students table */}
      <div>
        <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--navy)', marginBottom: 12 }}>
          قائمة الطلاب ({students.length})
        </div>
        <div style={{ background: '#fff', border: '1px solid var(--border)', borderRadius: 12, overflow: 'hidden' }}>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
              <thead>
                <tr style={{ background: 'var(--cream)', borderBottom: '1px solid var(--border)' }}>
                  {['#','الاسم','البريد الإلكتروني','النقاط','الدروس المكتملة','آخر نشاط'].map(h => (
                    <th key={h} style={{
                      padding: '10px 14px', textAlign: 'right',
                      fontSize: 11, fontWeight: 600, color: 'var(--muted)',
                      letterSpacing: '.04em',
                    }}>
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {students.length === 0 ? (
                  <tr>
                    <td colSpan={6} style={{ padding: 32, textAlign: 'center', color: 'var(--muted)', fontSize: 13 }}>
                      لا يوجد طلاب مسجّلون بعد.
                    </td>
                  </tr>
                ) : students.map((s, i) => (
                  <tr
                    key={s.student_id}
                    style={{ borderBottom: '1px solid var(--border)' }}
                    onMouseEnter={e => e.currentTarget.style.background = 'var(--cream)'}
                    onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                  >
                    <td style={{ padding: '10px 14px', color: 'var(--muted)', fontSize: 11 }}>{i + 1}</td>
                    <td style={{ padding: '10px 14px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 9 }}>
                        <div style={{
                          width: 30, height: 30, borderRadius: '50%', background: 'var(--gold)',
                          color: 'var(--navy)', display: 'flex', alignItems: 'center',
                          justifyContent: 'center', fontSize: 11, fontWeight: 700, flexShrink: 0,
                        }}>
                          {s.name?.[0] || '?'}
                        </div>
                        <span style={{ fontWeight: 500, color: 'var(--text)' }}>{s.name}</span>
                      </div>
                    </td>
                    <td style={{ padding: '10px 14px', color: 'var(--muted)', fontSize: 12 }} dir="ltr">
                      {s.email}
                    </td>
                    <td style={{ padding: '10px 14px' }}>
                      <span style={{ fontWeight: 700, color: 'var(--navy)', fontFamily: "'Amiri', serif", fontSize: 15 }}>
                        {s.total_score || 0}
                      </span>
                    </td>
                    <td style={{ padding: '10px 14px' }}>
                      <span style={{ fontWeight: 600, color: '#1D9E75' }}>{s.lessons_done || 0}</span>
                    </td>
                    <td style={{ padding: '10px 14px', color: 'var(--muted)', fontSize: 12 }} dir="ltr">
                      {s.last_active
                        ? new Date(s.last_active).toLocaleDateString('ar-EG', { day: 'numeric', month: 'short', year: 'numeric' })
                        : '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}
