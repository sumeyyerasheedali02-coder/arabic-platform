import { activities } from './language.js'
import { downloadCsv, format, total } from './format.js'

export default function ClassReport({ data, t, mutate }) {
  const rows = data.students.map(student => {
    const entries = data.entries.filter(e => e.student_id === student.id && total(e, activities) !== null)
    const weekly = entries.length ? entries.reduce((sum, e) => sum + total(e, activities), 0) / entries.length : null
    return { student, weekly, results: data.results[student.id] }
  })
  function exportCsv() {
    const headers = [t('number'), t('name'), t('section'), t('year'), ...activities.map(t),
      `${t('term')} 1 /100`, `${t('term')} 2 /100`, t('overall')]
    downloadCsv([headers, ...rows.map(({ student, results }) => {
      const entries = data.entries.filter(e => e.student_id === student.id && total(e, activities) !== null)
      return [student.student_number, student.name, data.cycle.section, data.cycle.academic_year,
        ...activities.map(a => entries.length ? (entries.reduce((sum, e) => sum + e[a], 0) / entries.length).toFixed(2) : ''),
        ...results.terms.map(r => r?.total), results.overall?.score]
    })], `takip-${data.cycle.academic_year}-${data.cycle.section}.csv`)
  }
  return <div className="kart"><div className="editor-heading"><div><h2>{t('report')}</h2><p className="alt">{t('finalInfo')}</p></div><button className="dugme ikincil" onClick={exportCsv} disabled={!rows.length}>{t('csv')}</button></div>
    <p className="bilgi">{t('termInfo')}</p><div className="tablo-kutu"><table><thead><tr><th>{t('number')}</th><th>{t('name')}</th><th className="veri">{t('percentage')}</th><th className="veri">{t('term')} 1 /100</th><th className="veri">{t('term')} 2 /100</th><th className="veri">{t('overall')}</th><th>{t('needed')}</th></tr></thead><tbody>{rows.map(({ student, weekly, results }) => <tr key={student.id}><td className="no" dir="ltr">{student.student_number || '—'}</td><td className="ad">{student.name}</td><td className="veri">{format(weekly == null ? null : weekly / 40 * 100)}%</td>{results.terms.map((r, i) => <td className="veri" key={i}>{format(r?.total)}</td>)}<td className="veri"><strong>{format(results.overall?.score)}</strong><br /><span className={results.overall?.passed ? 'n-iyi' : 'n-dusuk'}>{t(results.overall ? results.overall.passed ? 'passed' : 'risk' : 'incomplete')}</span></td><td className="veri">{format(results.overall?.needed)}</td></tr>)}</tbody></table></div>
    <div className="actions"><span className={`etiket ${data.cycle.final_published ? 'e-yayin' : 'e-taslak'}`}>{t(data.cycle.final_published ? 'published' : 'draft')}</span><button className="dugme" onClick={() => mutate('/final-publication', 'PATCH', { published: !data.cycle.final_published })}>{t(data.cycle.final_published ? 'finalUnpublish' : 'finalPublish')}</button></div>
  </div>
}
