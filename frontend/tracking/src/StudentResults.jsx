import { useState } from 'react'
import { useResource } from './api.js'
import { activities } from './language.js'
import { format, scoreClass, total } from './format.js'

export default function StudentResults({ cycleId, token, t }) {
  const [revision, setRevision] = useState(0)
  const resource = useResource(`/tracking/cycles/${cycleId}/me`, token, revision)
  const data = resource.data
  if (resource.loading) return <p className="bos">{t('loading')}</p>
  if (resource.error) return <div className="uyari" role="alert">{resource.error}<button className="dugme" onClick={() => setRevision(v => v + 1)}>{t('refreshed')}</button></div>
  const entries = data.entries
  const sum = entries.reduce((sum, e) => sum + total(e, activities), 0)
  const percent = entries.length ? sum / (entries.length * 40) * 100 : null
  return <><div className="kart"><div className="editor-heading"><h2>{data.students[0].name}</h2><button className="dugme ikincil ufak" onClick={() => setRevision(v => v + 1)}>{t('refreshed')}</button></div>
    {!entries.length ? <p className="bos">{t('noResults')}</p> : <><div className="ozet"><div><span className="alt">{t('total')}</span><b>{format(sum)}<small>/{entries.length * 40}</small></b></div><div><span className="alt">{t('percentage')}</span><b className={`n-${scoreClass(percent)}`}>{format(percent)}%</b></div><div><span className="alt">{t('assessed')}</span><b>{entries.length}</b></div></div>
    <p className="goz">{t('averages')}</p><table><tbody>{activities.map(a => {
      const mean = entries.reduce((sum, e) => sum + e[a], 0) / entries.length
      return <tr key={a}><td>{t(a)}</td><td className="veri" dir="ltr">{format(mean)} /10</td><td><div className="cubuk"><i className={`p-${scoreClass(mean * 10)}`} style={{ width: `${mean * 10}%` }} /></div></td></tr>
    })}</tbody></table></>}</div>
    {entries.length > 0 && <div className="kart"><h2>{t('weeks')}</h2><div className="tablo-kutu"><table><thead><tr><th>{t('week')}</th>{activities.map(a => <th key={a} className="veri">{t(a)}</th>)}<th className="veri">{t('total')} /40</th></tr></thead><tbody>{data.weeks.filter(w => entries.some(e => e.week_id === w.id)).map(w => {
      const e = entries.find(e => e.week_id === w.id)
      return <tr key={w.id}><td>{w.number}<br /><small>{w.starts_on}</small></td>{activities.map(a => <td key={a} className={`veri n-${scoreClass(e[a] * 10)}`}>{format(e[a])}</td>)}<td className="veri">{format(total(e, activities))}</td></tr>
    })}</tbody></table></div></div>}
    {data.results.terms.map((r, index) => r && <div className="kart" key={index}><p className="goz">{t('term')} {index + 1}</p><div className="ozet"><div><span className="alt">{t('activity')}</span><b>{format(r.activity)}</b></div><div><span className="alt">{t('exam')}</span><b>{format(r.exam)}</b></div><div><span className="alt">{t('total')} /100</span><b>{format(r.total)}</b></div></div></div>)}
    {data.results.overall && <div className="kart"><h2>{t('overall')}</h2><div className="ozet"><div><b>{format(data.results.overall.score)}</b></div><div><b className={data.results.overall.passed ? 'n-iyi' : 'n-dusuk'}>{t(data.results.overall.passed ? 'passed' : 'risk')}</b></div></div><p className="alt">{t('finalInfo')}</p></div>}
    {entries.some(e => e.note.trim()) && <div className="kart"><h2>{t('note')}</h2>{entries.filter(e => e.note.trim()).map(e => <p className="not-kutu" key={e.week_id}><strong>{t('week')} {data.weeks.find(w => w.id === e.week_id).number} — </strong>{e.note}</p>)}</div>}
  </>
}
