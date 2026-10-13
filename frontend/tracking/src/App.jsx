import { useEffect, useState } from 'react'
import { request, TOKEN_KEY, useResource } from './api.js'
import { translate } from './language.js'
import StaffDashboard from './StaffDashboard.jsx'
import StudentResults from './StudentResults.jsx'

function Login({ t, onLogin }) {
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError('')
    const form = new FormData(event.currentTarget)
    try {
      const session = await request('/auth/login', null, { method: 'POST', body: new URLSearchParams({
        username: form.get('username').trim(), password: form.get('password'),
      }) })
      onLogin(session)
    } catch (e) { setError(e.message) } finally { setBusy(false) }
  }
  return <div className="login-wrap"><div className="hero">
    <p className="goz">{t('faculty')}</p><h1>{t('title')}</h1><p className="alt">{t('formula')}</p>
    <span className="hero-ar" aria-hidden="true">ع</span>
  </div><form className="kart login-form" onSubmit={submit}>
    <h2>{t('login')}</h2><p className="alt">{t('loginInfo')}</p>
    <label htmlFor="username">{t('identifier')}</label>
    <input id="username" name="username" autoComplete="username" dir="ltr" required />
    <label htmlFor="password">{t('password')}</label>
    <input id="password" name="password" type="password" autoComplete="current-password" required />
    {error && <p className="uyari" role="alert">{error}</p>}
    <button className="dugme" disabled={busy}>{busy ? t('loading') : t('login')}</button>
  </form></div>
}

function Profile({ account, token, t, onComplete }) {
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError('')
    const form = new FormData(event.currentTarget)
    try {
      onComplete(await request('/auth/me/profile', token, { method: 'PATCH', body: {
        student_number: account.student_number || form.get('number'),
        class_section: account.class_section || form.get('section'),
      } }))
    } catch (e) { setError(e.message) } finally { setBusy(false) }
  }
  return <form className="kart profile-form" onSubmit={submit}><h1>{t('profile')}</h1><p className="alt">{t('profileInfo')}</p>
    {!account.student_number && <><label htmlFor="number">{t('number')}</label><input name="number" id="number" inputMode="numeric" maxLength="32" required dir="ltr" /></>}
    {!account.class_section && <><label htmlFor="section">{t('section')}</label><select id="section" name="section" required defaultValue=""><option value="" disabled>—</option>{['A', 'B', 'C', 'D'].map(s => <option key={s}>{s}</option>)}</select></>}
    {error && <p className="uyari" role="alert">{error}</p>}<button className="dugme" disabled={busy}>{t('save')}</button>
  </form>
}

function Workspace({ account, token, t, dirty, onDirty: setDirty }) {
  const [revision, setRevision] = useState(0)
  const [chosen, setChosen] = useState(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const resource = useResource('/tracking/cycles', token, revision)
  const data = resource.data
  const cycles = data?.cycles || []
  const cycle = cycles.find(c => c.id === chosen) || cycles[0]
  const isStaff = account.role !== 'student'
  useEffect(() => {
    if (!dirty) return
    const warn = event => { event.preventDefault(); event.returnValue = '' }
    window.addEventListener('beforeunload', warn)
    return () => window.removeEventListener('beforeunload', warn)
  }, [dirty])
  function selectCycle(id) {
    if (dirty && !window.confirm(t('discard'))) return
    setDirty(false)
    setChosen(id)
  }
  async function create(event) {
    event.preventDefault()
    if (dirty && !window.confirm(t('discard'))) return
    const form = new FormData(event.currentTarget)
    setBusy(true)
    setError('')
    try {
      const created = await request('/tracking/cycles', token, { method: 'POST', body: {
        academic_year: form.get('year'), section: form.get('section'),
      } })
      setDirty(false)
      setChosen(created.id)
      setRevision(r => r + 1)
    } catch (e) { setError(e.message) } finally { setBusy(false) }
  }
  const currentYear = new Date().getFullYear() - (new Date().getMonth() < 8 ? 1 : 0)
  if (resource.loading) return <p className="bos">{t('loading')}</p>
  if (resource.error) return <div role="alert" className="uyari">{resource.error}<button className="dugme ufak" onClick={() => setRevision(r => r + 1)}>{t('refreshed')}</button></div>
  return <>
    <div className="page-heading"><div><p className="goz">{t(account.role)} · {account.name}</p><h1>{t('title')}</h1><p className="alt">{t('formula')}</p></div></div>
    {cycles.length > 0 && <div className="cycle-selector"><label htmlFor="cycle">{t('year')} · {t('section')}</label>
      <select id="cycle" value={cycle?.id || ''} onChange={e => selectCycle(Number(e.target.value))}>{cycles.map(c => <option value={c.id} key={c.id}>{c.academic_year} · {t('section')} {c.section}</option>)}</select>
    </div>}
    {isStaff && data?.sections.length > 0 && <details className="kart cycle-create"><summary>{t('newCycle')}</summary><form className="satir" onSubmit={create}>
      <div><label htmlFor="year">{t('year')}</label><input id="year" name="year" dir="ltr" pattern="20[0-9]{2}-20[0-9]{2}" defaultValue={`${currentYear}-${currentYear + 1}`} required /></div>
      <div><label htmlFor="create-section">{t('section')}</label><select id="create-section" name="section">{data.sections.map(s => <option key={s}>{s}</option>)}</select></div>
      <button className="dugme" disabled={busy}>{t('add')}</button></form>{error && <p className="uyari" role="alert">{error}</p>}</details>}
    {isStaff && !data?.sections.length && <div className="bilgi">{t('noSections')}</div>}
    {!cycle && <p className="bos">{t('noCycles')}</p>}
    {cycle && (isStaff ? <StaffDashboard key={cycle.id} cycleId={cycle.id} token={token} t={t} dirty={dirty} onDirty={setDirty} />
      : <StudentResults key={cycle.id} cycleId={cycle.id} token={token} t={t} />)}
  </>
}

export default function App() {
  const [lang, setLang] = useState(() => localStorage.getItem('takip-language') || 'tr')
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY))
  const [account, setAccount] = useState(null)
  const [initialError, setInitialError] = useState('')
  const [dirty, setDirty] = useState(false)
  const t = translate(lang)
  useEffect(() => {
    document.documentElement.lang = lang
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr'
    localStorage.setItem('takip-language', lang)
    document.title = t('title')
  }, [lang, t])
  useEffect(() => {
    if (!token) return
    const controller = new AbortController()
    request('/auth/me', token, { signal: controller.signal }).then(
      data => { if (!controller.signal.aborted) setAccount(data) },
      e => { if (!controller.signal.aborted) setInitialError(e.message) },
    )
    return () => controller.abort()
  }, [token])
  useEffect(() => {
    function expired() { localStorage.removeItem(TOKEN_KEY); setToken(null); setAccount(null); setDirty(false) }
    window.addEventListener('takip-session-expired', expired)
    return () => window.removeEventListener('takip-session-expired', expired)
  }, [])
  function login(session) {
    localStorage.setItem(TOKEN_KEY, session.access_token)
    setInitialError('')
    setAccount(session)
    setToken(session.access_token)
  }
  function logout() {
    if (dirty && !window.confirm(t('discard'))) return
    localStorage.removeItem(TOKEN_KEY)
    setToken(null)
    setAccount(null)
    setInitialError('')
    setDirty(false)
  }
  return <><header className="bant"><div className="bant-ic"><div className="logo"><b>{t('title')}</b><span>{t('faculty')}</span></div>
    <div className="header-actions"><button className="dugme ufak" onClick={() => setLang(lang === 'ar' ? 'tr' : 'ar')}>{lang === 'ar' ? 'Türkçe' : 'العربية'}</button>
      {token && <button className="dugme ufak" onClick={logout}>{t('logout')}</button>}</div>
  </div></header><main className="kabuk">
    {!token ? <Login t={t} onLogin={login} /> : !account ? <div className="bos">{initialError || t('loading')}{initialError && <button className="dugme" onClick={logout}>{t('login')}</button>}</div>
      : account.role === 'student' && (!account.class_section || !account.student_number)
        ? <Profile t={t} account={account} token={token} onComplete={setAccount} /> : <Workspace t={t} account={account} token={token} dirty={dirty} onDirty={setDirty} />}
  </main></>
}
