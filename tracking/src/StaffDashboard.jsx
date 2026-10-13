import { useState } from 'react'
import { request, useResource } from './api.js'
import GradeEditor from './GradeEditor.jsx'
import TermEditor from './TermEditor.jsx'
import ClassReport from './ClassReport.jsx'

export default function StaffDashboard({ cycleId, token, t, dirty, onDirty }) {
  const [version, setVersion] = useState(0)
  const [tab, setTab] = useState('grades')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [saved, setSaved] = useState(false)
  const [selectedWeek, setSelectedWeek] = useState(null)
  const [selectedTerm, setSelectedTerm] = useState(1)
  const resource = useResource(`/tracking/cycles/${cycleId}/state`, token, version)
  const data = resource.data
  async function mutate(path, method, body) {
    setBusy(true)
    setError('')
    setSaved(false)
    try {
      await request(`/tracking/cycles/${cycleId}${path}`, token, { method, body: { ...body, revision: data.cycle.revision } })
      onDirty(false)
      setVersion(v => v + 1)
      setSaved(true)
    } catch (e) { setError(e.message) } finally { setBusy(false) }
  }
  function navigate(next) {
    if (dirty && !window.confirm(t('discard'))) return
    onDirty(false)
    setTab(next)
    setSaved(false)
    setError('')
  }
  function refresh() {
    if (dirty && !window.confirm(t('discard'))) return
    onDirty(false)
    setVersion(v => v + 1)
    setError('')
  }
  if (resource.loading) return <p className="bos">{t('loading')}</p>
  if (resource.error) return <div className="uyari" role="alert">{resource.error}<button className="dugme" onClick={refresh}>{t('refreshed')}</button></div>
  return <><nav className="sekmeler" aria-label={t('title')}>
    {['grades', 'weeks', 'terms', 'report', 'audit'].map(key => <button key={key} aria-current={tab === key ? 'page' : undefined} aria-selected={tab === key} onClick={() => navigate(key)} disabled={busy}>{t(key)}</button>)}
    <button className="refresh-button" disabled={busy} onClick={refresh}>{t('refreshed')}</button>
  </nav>{error && <p className="uyari" role="alert">{error}</p>}{saved && <p className="bilgi" role="status">{t('saved')}</p>}
    <fieldset className="workspace-fieldset" disabled={busy}>
      {tab === 'grades' && <GradeEditor key={`${cycleId}:${data.cycle.revision}`} data={data} t={t} mutate={mutate} onDirty={onDirty} dirty={dirty} selectedWeek={selectedWeek} onWeek={setSelectedWeek} />}
      {tab === 'weeks' && <Weeks data={data} t={t} mutate={mutate} />}
      {tab === 'terms' && <TermEditor key={`${cycleId}:${data.cycle.revision}`} data={data} t={t} mutate={mutate} onDirty={onDirty} dirty={dirty} selectedTerm={selectedTerm} onTerm={setSelectedTerm} />}
      {tab === 'report' && <ClassReport data={data} t={t} mutate={mutate} />}
      {tab === 'audit' && <div className="kart"><h2>{t('audit')}</h2><div className="tablo-kutu"><table><thead><tr><th>{t('date')}</th><th>{t('teacher')}</th><th>{t('audit')}</th></tr></thead><tbody>{data.audit.map(a => <tr key={a.id}><td>{new Date(a.created_at.replace(/Z$/, '') + 'Z').toLocaleString()}</td><td>{a.actor}</td><td>{t(a.action)}</td></tr>)}</tbody></table></div></div>}
    </fieldset><p className="alt">{t('sharedAccounts')}</p></>
}

function Weeks({ data, t, mutate }) {
  function add(event) {
    event.preventDefault()
    const form = new FormData(event.currentTarget)
    mutate('/weeks', 'POST', { number: Number(form.get('number')), starts_on: form.get('date') })
  }
  return <><form className="kart" onSubmit={add}><h2>{t('newWeek')}</h2><div className="satir">
    <div><label htmlFor="week-number">{t('week')}</label><input id="week-number" type="number" name="number" min="1" max="52" required defaultValue={Math.max(0, ...data.weeks.map(w => w.number)) + 1} /></div>
    <div><label htmlFor="week-date">{t('date')}</label><input id="week-date" type="date" name="date" required /></div><button className="dugme">{t('add')}</button></div></form>
    <div className="kart"><div className="tablo-kutu"><table><thead><tr><th>{t('week')}</th><th>{t('date')}</th><th>{t('published')}</th><th></th></tr></thead><tbody>{data.weeks.map(w => <tr key={w.id}><td>{w.number}</td><td>{w.starts_on}</td><td><span className={`etiket ${w.published ? 'e-yayin' : 'e-taslak'}`}>{t(w.published ? 'published' : 'draft')}</span></td><td><button className="dugme ufak ikincil" onClick={() => mutate(`/weeks/${w.id}/publication`, 'PATCH', { published: !w.published })}>{t(w.published ? 'unpublish' : 'publish')}</button></td></tr>)}</tbody></table></div></div></>
}
