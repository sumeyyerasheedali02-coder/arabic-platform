/** Native selection makes all 48 units reachable without a long horizontal swipe. */
export default function UnitPicker({ units, selectedId, onSelect }) {
  return (
    <div className="lessons-units mobile-unit-picker">
      <label htmlFor="lesson-unit">الوحدة الدراسية</label>
      <select id="lesson-unit" value={selectedId ?? ''} onChange={event => {
        const unit = units.find(item => String(item.id) === event.target.value)
        if (unit) onSelect(unit)
      }}>
        {!selectedId && <option value="" disabled>اختر وحدة</option>}
        {units.map(unit => <option key={unit.id} value={unit.id}>{unit.unit_number}. {unit.title_ar}</option>)}
      </select>
    </div>
  )
}
