import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../api/client'

const AR_NUMS = ['١','٢','٣','٤','٥','٦','٧','٨','٩','١٠']

function KBULogo() {
  return (
    <svg width="32" height="32" viewBox="0 0 32 32">
      <circle cx="16" cy="16" r="15" fill="none" stroke="#C9A84C" strokeWidth="1.5" />
      <circle cx="16" cy="16" r="10" fill="none" stroke="#C9A84C" strokeWidth="1" opacity=".5" />
      <text x="16" y="20" textAnchor="middle" fill="#C9A84C" fontSize="9" fontWeight="700"
        fontFamily="DM Sans, sans-serif" letterSpacing=".05em">KBÜ</text>
    </svg>
  )
}

export default function Sidebar({ selectedUnit, onSelectUnit }) {
  const { student, logout, token } = useAuth()
  const navigate = useNavigate()
  const [units, setUnits]         = useState([])
  const [progress, setProgress]   = useState([])

  useEffect(() => {
    api.get('/units').then(r => setUnits(r.data)).catch(console.error)
    if (token) {
      api.get('/me/progress').then(r => setProgress(r.data)).catch(console.error)
    }
  }, [token])

  const totalLessons    = units.reduce((s, u) => s + (u.total_lessons || 0), 0)
  const doneLessons     = progress.filter(p => p.status === 'completed').length
  const progressPct     = totalLessons > 0 ? Math.round((doneLessons / totalLessons) * 100) : 0

  return (
    <aside className="app-sidebar" style={{
      background: 'var(--navy)',
      display: 'flex',
      flexDirection: 'column',
      borderLeft: '1px solid rgba(255,255,255,.06)',
    }}>
      {/* KBU + Researcher */}
      <div style={{ padding: '20px 18px 16px', borderBottom: '1px solid rgba(201,168,76,.2)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
          <KBULogo />
          <div>
            <div style={{ fontSize: 11, color: '#fff', fontWeight: 500 }}>Karabük Üniversitesi</div>
            <div style={{ fontSize: 9, color: 'rgba(255,255,255,.4)', letterSpacing: '.06em' }}>
              İLAHİYAT FAKÜLTESİ
            </div>
          </div>
        </div>
        <div style={{
          background: 'rgba(201,168,76,.08)',
          border: '1px solid rgba(201,168,76,.2)',
          borderRadius: 9, padding: '10px 12px',
        }}>
          <div style={{ fontSize: 9, color: '#C9A84C', letterSpacing: '.1em', fontWeight: 500, marginBottom: 3 }}>
            RESEARCHER
          </div>
          <div style={{ fontSize: 12.5, fontWeight: 500, color: '#fff' }}>MUSTAFA AHMED</div>
          <div style={{ fontSize: 9, color: 'rgba(255,255,255,.4)', marginTop: 2 }}>
            AI &amp; Language Technology · M.Sc.
          </div>
        </div>
      </div>

      {/* Units list */}
      <nav style={{ flex: 1, overflowY: 'auto', padding: '12px 0 4px' }}>
        <div style={{
          fontSize: 9, letterSpacing: '.12em', color: 'rgba(255,255,255,.3)',
          padding: '0 16px 8px', fontWeight: 500,
        }}>
          UNITS — الوحدات
        </div>

        {units.map((unit, i) => {
          const isActive = selectedUnit?.id === unit.id
          return (
            <div
              key={unit.id}
              onClick={() => onSelectUnit(unit)}
              style={{
                display: 'flex', alignItems: 'flex-start', gap: 10,
                padding: '9px 16px', cursor: 'pointer',
                borderRight: isActive ? '3px solid #C9A84C' : '3px solid transparent',
                background: isActive ? 'rgba(201,168,76,.1)' : 'transparent',
                transition: 'all .18s',
              }}
              onMouseEnter={e => { if (!isActive) e.currentTarget.style.background = 'rgba(201,168,76,.05)' }}
              onMouseLeave={e => { if (!isActive) e.currentTarget.style.background = 'transparent' }}
            >
              <div style={{
                width: 22, height: 22, borderRadius: 6, flexShrink: 0,
                background: isActive ? '#C9A84C' : 'rgba(255,255,255,.08)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 10, fontWeight: 500,
                color: isActive ? 'var(--navy)' : 'rgba(255,255,255,.6)',
              }}>
                {AR_NUMS[i] || i + 1}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{
                  fontSize: 11, fontFamily: "'Amiri', serif",
                  color: isActive ? '#fff' : 'rgba(255,255,255,.8)',
                  whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
                }}>
                  {unit.title_ar}
                </div>
                <div style={{ fontSize: 9, color: 'rgba(255,255,255,.35)', marginTop: 1 }}>
                  {unit.title_tr}
                </div>
              </div>
            </div>
          )
        })}
      </nav>

      {/* Overall progress */}
      <div style={{ padding: 16, borderTop: '1px solid rgba(255,255,255,.06)' }}>
        <div style={{ background: 'rgba(255,255,255,.06)', borderRadius: 9, padding: '10px 12px', marginBottom: 10 }}>
          <div style={{ fontSize: 9, color: 'rgba(255,255,255,.4)', marginBottom: 6, letterSpacing: '.08em' }}>
            OVERALL PROGRESS
          </div>
          <div style={{ height: 4, background: 'rgba(255,255,255,.12)', borderRadius: 2, overflow: 'hidden' }}>
            <div style={{ height: '100%', background: '#C9A84C', borderRadius: 2, width: `${progressPct}%`, transition: 'width .4s' }} />
          </div>
          <div style={{ fontSize: 11, color: '#C9A84C', marginTop: 5, fontWeight: 500 }}>
            {progressPct}% مكتمل
          </div>
        </div>

        {/* Student info + logout / guest */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <div style={{
            width: 28, height: 28, borderRadius: '50%',
            background: student ? '#C9A84C' : 'rgba(255,255,255,.15)',
            color: student ? 'var(--navy)' : 'rgba(255,255,255,.6)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 10, fontWeight: 700, flexShrink: 0,
            border: student ? 'none' : '1px solid rgba(255,255,255,.2)',
          }}>
            {student ? student.name.split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase() : '؟'}
          </div>
          <div style={{ flex: 1, minWidth: 0 }}>
            {student ? (
              <div style={{ fontSize: 11, color: '#fff', fontWeight: 500, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {student.name}
              </div>
            ) : (
              <>
                <div style={{ fontSize: 11, color: 'rgba(255,255,255,.55)', fontWeight: 500 }}>ضيف</div>
                <div style={{ fontSize: 9, color: 'rgba(255,255,255,.25)', marginTop: 1 }}>Guest Mode</div>
              </>
            )}
          </div>
          <button
            onClick={() => { logout(); navigate('/login') }}
            style={{
              background: 'none', border: '1px solid rgba(255,255,255,.15)',
              borderRadius: 6, cursor: 'pointer', padding: '3px 7px',
              color: 'rgba(255,255,255,.45)', fontSize: 10,
              fontFamily: 'DM Sans, sans-serif', transition: 'all .15s',
            }}
            title={student ? 'تسجيل الخروج' : 'تسجيل الدخول'}
            onMouseEnter={e => { e.currentTarget.style.background = 'rgba(255,255,255,.08)'; e.currentTarget.style.color = '#fff' }}
            onMouseLeave={e => { e.currentTarget.style.background = 'none'; e.currentTarget.style.color = 'rgba(255,255,255,.45)' }}
          >
            {student ? 'خروج' : 'دخول'}
          </button>
        </div>
      </div>
    </aside>
  )
}
