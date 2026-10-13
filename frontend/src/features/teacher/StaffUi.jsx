import './staff.css'

export function StaffMessage({ error, onRetry }) {
  return <div className="staff-message" role="alert">
    <p>{error}</p>
    {onRetry && <button type="button" onClick={onRetry}>إعادة المحاولة</button>}
  </div>
}

export function StaffStats({ items }) {
  return <div className="staff-stats">
    {items.map(([label, value]) => <div className="staff-stat" key={label}>
      <span>{label}</span><strong>{value}</strong>
    </div>)}
  </div>
}

export function CompletionBar({ value }) {
  return <div className="staff-completion">
    <span>{value ?? 0}%</span>
    <div className="staff-progress"><i style={{ width: `${Math.min(100, value ?? 0)}%` }} /></div>
  </div>
}
