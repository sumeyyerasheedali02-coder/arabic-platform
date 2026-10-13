import { useState } from 'react'
import { format, markValue } from './format.js'

function initial(data, number) {
  const term = data.terms.find(term => term.number === number)
  return { first: term?.first_week ?? '', last: term?.last_week ?? '',
    scores: Object.fromEntries(data.students.map(s => [s.id, data.exams.find(e => e.term_id === term?.id && e.student_id === s.id)?.score ?? null])) }
}

export default function TermEditor({ data, t, mutate, onDirty, dirty, selectedTerm, onTerm }) {
  const [number, setNumber] = useState(selectedTerm)
  const [values, setValues] = useState(() => initial(data, selectedTerm))
  const term = data.terms.find(term => term.number === number)
  function change(key, value) { setValues(v => ({ ...v, [key]: value })); onDirty(true) }
  function select(n) {
    if (dirty && !window.confirm(t('discard'))) return
    setNumber(n)
    onTerm(n)
    setValues(initial(data, n))
    onDirty(false)
  }
  function save(event) {
    event.preventDefault()
    mutate(`/terms/${number}`, 'PUT', { first_week: Number(values.first), last_week: Number(values.last),
      publish: event.nativeEvent.submitter?.value === 'publish',
      entries: data.students.map(s => ({ student_id: s.id, score: values.scores[s.id] })),
    })
  }
  return <form className="kart" onSubmit={save}><div className="satir"><div><label htmlFor="term">{t('term')}</label><select id="term" value={number} onChange={e => select(Number(e.target.value))}><option value="1">1</option><option value="2">2</option></select></div>
    <div><label htmlFor="first-week">{t('firstWeek')}</label><input id="first-week" type="number" min="1" max="52" value={values.first} required onChange={e => change('first', e.target.value)} /></div>
    <div><label htmlFor="last-week">{t('lastWeek')}</label><input id="last-week" type="number" min={Number(values.first) || 1} max="52" value={values.last} required onChange={e => change('last', e.target.value)} /></div>
    <span className={`etiket ${term?.published ? 'e-yayin' : 'e-taslak'}`}>{t(term?.published ? 'published' : 'draft')}</span></div><p className="bilgi">{t('termInfo')}</p>
    <div className="tablo-kutu"><table><thead><tr><th>{t('number')}</th><th>{t('name')}</th><th className="veri">{t('activity')}</th><th className="veri">{t('exam')}</th><th className="veri">{t('total')} /100</th></tr></thead><tbody>{data.students.map(s => {
      const result = data.results[s.id]?.terms[number - 1]
      const sameRange = term?.first_week === Number(values.first) && term?.last_week === Number(values.last)
      const activity = sameRange ? result?.activity : null
      const score = values.scores[s.id]
      return <tr key={s.id}><td className="no" dir="ltr">{s.student_number || '—'}</td><td className="ad">{s.name}</td><td className="veri">{format(activity)}</td><td className="veri"><input type="number" min="0" max="60" step="any" aria-label={`${s.name} · ${t('exam')}`} value={score ?? ''} onChange={e => change('scores', { ...values.scores, [s.id]: markValue(e.target.value) })} /></td><td className="veri">{format(activity == null || score == null ? null : activity + score)}</td></tr>
    })}</tbody></table></div><div className="actions"><button className="dugme ikincil" value="draft">{t('save')}</button><button className="dugme" value="publish">{t('savePublish')}</button>
      {term?.published && <button className="dugme sade" value="draft">{t('unpublish')}</button>}</div></form>
}
