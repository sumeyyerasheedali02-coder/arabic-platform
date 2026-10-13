/** Mobile unit chooser above the lessons; desktop uses the navy sidebar. */
export default function UnitPicker({ units, selectedId, onSelect }) {
  return (
    <aside className="lessons-units" style={{ width: 200, flexShrink: 0 }}>
      <div style={{ fontSize: 9, letterSpacing: '.1em', color: 'var(--muted)', fontWeight: 500, marginBottom: 10 }}>
        الوحدات الدراسية
      </div>
      <div className="lessons-units-list" style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
        {units.map(unit => {
          const isActive = selectedId === unit.id
          return (
            <button
              key={unit.id}
              className="lessons-unit-btn"
              onClick={() => onSelect(unit)}
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
  )
}
