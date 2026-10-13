import { useState } from 'react'
import { activities } from './language.js'
import { format, markValue, total } from './format.js'

function initialEntries(data, weekId) {
  return Object.fromEntries(data.students.map(s => [s.id, {
    student_id: s.id, ...Object.fromEntries(activities.map(a => [a, null])), note: '',
    ...data.entries.find(e => e.student_id === s.id && e.week_id === weekId),
  }]))
}

export default function GradeEditor({ data, t, mutate, onDirty, dirty, selectedWeek, onWeek }) {
  const initialWeek = data.weeks.find(w => w.id === selectedWeek)?.id || data.weeks[0]?.id
  const [weekId, setWeekId] = useState(initialWeek)
  const [entries, setEntries] = useState(() => initialEntries(data, initialWeek))
  const week = data.weeks.find(w => w.id === weekId)
  function select(id) {
    if (dirty && !window.confirm(t('discard'))) return
    setWeekId(id)
    onWeek(id)
    setEntries(initialEntries(data, id))
    onDirty(false)
  }
  function change(id, key, value) {
    setEntries(current => ({ ...current, [id]: { ...current[id], [key]: value } }))
    onDirty(true)
  }
  function save(event, publish) {
    event.preventDefault()
    // Both save buttons must enforce the HTML numeric constraints.
    if (!event.currentTarget.form.checkValidity()) { event.currentTarget.form.reportValidity(); return }
    mutate(`/weeks/${weekId}`, 'PUT', { publish, entries: Object.values(entries).map(e => {
      const { week_id: _ignored, ...values } = e
      return values
    }) })
  }
  if (!week) return <div className="bos">{t('noWeeks')}</div>
  return <form className="kart" onSubmit={e => e.preventDefault()}><div className="editor-heading"><div><label htmlFor="selected-week">{t('week')}</label><select id="selected-week" value={weekId} onChange={e => select(Number(e.target.value))}>{data.weeks.map(w => <option key={w.id} value={w.id}>{w.number} · {w.starts_on}</option>)}</select></div>
    <span className={`etiket ${week.published ? 'e-yayin' : 'e-taslak'}`}>{t(week.published ? 'published' : 'draft')}</span></div>
    <p className="bilgi">{t('draftInfo')}</p>
    {data.students.length === 0 ? <p className="bos">{t('emptyStudents')}</p> : <><div className="tablo-kutu"><table className="grade-table"><thead><tr><th>{t('number')}</th><th>{t('name')}</th>{activities.map(a => <th key={a} className="veri">{t(a)} /10</th>)}<th className="veri">{t('total')} /40</th><th>{t('note')}</th></tr></thead><tbody>
      {data.students.map(s => <tr key={s.id}><td className="no" dir="ltr">{s.student_number || t('missingNumber')}</td><td className="ad">{s.name}</td>{activities.map(a => <td key={a}><input type="number" min="0" max="10" step="any" aria-label={`${s.name} · ${t(a)}`} value={entries[s.id][a] ?? ''} onChange={e => change(s.id, a, markValue(e.target.value))} /></td>)}<td className="veri">{format(total(entries[s.id], activities))}</td><td><input type="text" aria-label={`${s.name} · ${t('note')}`} maxLength="2000" value={entries[s.id].note} onChange={e => change(s.id, 'note', e.target.value)} /></td></tr>)}
    </tbody></table></div><div className="actions"><button className="dugme ikincil" onClick={e => save(e, false)}>{t('save')}</button><button className="dugme" onClick={e => save(e, true)}>{t('savePublish')}</button></div></>}
  </form>
}
