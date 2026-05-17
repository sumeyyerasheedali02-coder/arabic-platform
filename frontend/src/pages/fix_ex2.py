import os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages")

m = open("Exercises.jsx", encoding="utf-8").read()

old = "  const [exercises, setExercises]     = useState([])"
new = """  const [allExercises, setAllExercises] = useState([])
  const [exercises, setExercises]       = useState([])
  const [filter, setFilter]             = useState('all')"""
m = m.replace(old, new)

old2 = "    api.get(`/units/${selectedUnit.id}/exercises`)\n      .then(r => setExercises(r.data))"
new2 = """    api.get(`/units/${selectedUnit.id}/exercises`)
      .then(r => { setAllExercises(r.data); setExercises(r.data) })"""
m = m.replace(old2, new2)

old3 = "  const handleAnswer = (result) => setSession(s => [...s, result])"
new3 = """  useEffect(() => {
    const filtered = allExercises.filter(ex => matchesFilter(ex, filter))
    setExercises(filtered)
    setCurrent(0)
    setSession([])
    setDone(false)
  }, [filter, allExercises])

  const handleAnswer = (result) => setSession(s => [...s, result])"""
m = m.replace(old3, new3)

old4 = "      <h1 style={{ fontSize: 17, fontWeight: 700, color: 'var(--navy)', margin: 0 }}>Ø§Ù„ØªÙ…Ø§Ø±ÙŠÙ†</h1>"
new4 = """      <h1 style={{ fontSize: 17, fontWeight: 700, color: 'var(--navy)', margin: 0 }}>\u0627\u0644\u062a\u0645\u0627\u0631\u064a\u0646</h1>"""
m = m.replace(old4, new4)

filter_ui = """
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 16 }}>
        {FILTER_OPTIONS.map(opt => (
          <button key={opt.value} onClick={() => setFilter(opt.value)} style={{
            padding: '4px 10px', borderRadius: 20, border: 'none', cursor: 'pointer',
            fontSize: 11, fontWeight: 600, fontFamily: 'DM Sans, sans-serif',
            background: filter === opt.value ? 'var(--navy)' : 'var(--cream)',
            color: filter === opt.value ? '#fff' : 'var(--navy)',
          }}>
            {opt.label} ({allExercises.filter(ex => matchesFilter(ex, opt.value)).length})
          </button>
        ))}
      </div>
"""

old5 = "      {loadingEx ? ("
new5 = filter_ui + "\n      {loadingEx ? ("
m = m.replace(old5, new5, 1)

open("Exercises.jsx", "w", encoding="utf-8").write(m)
print("Done!")
