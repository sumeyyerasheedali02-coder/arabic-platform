import { useEffect, useState } from 'react'
import api from '../../api/client'
import { useAuth } from '../../auth/useAuth'
import { CenteredSpinner } from '../../components/Spinner'
import LessonCard from './LessonCard'
import LessonPanel from './LessonPanel'
import UnitHeader from './UnitHeader'
import UnitPicker from './UnitPicker'
import { VocabularyList } from './VocabularyRow'

const PAGE_TABS = [['lessons', 'الدروس'], ['vocab', 'المفردات']]

export default function LessonsPage() {
  const { token }                           = useAuth()
  const [units, setUnits]                   = useState([])
  const [selectedUnit, setSelectedUnit]     = useState(null)
  const [lessons, setLessons]               = useState([])
  const [vocab, setVocab]                   = useState([])
  const [tab, setTab]                       = useState('lessons')
  const [srsMsg, setSrsMsg]                 = useState('')
  const [loadingUnits, setLoadingUnits]     = useState(true)
  const [loadingContent, setLoadingContent] = useState(false)
  const [openLesson, setOpenLesson]         = useState(null)

  useEffect(() => {
    api.get('/units').then(r => {
      setUnits(r.data)
      if (r.data[0]) setSelectedUnit(r.data[0])
    }).finally(() => setLoadingUnits(false))
  }, [])

  useEffect(() => {
    if (!selectedUnit) return
    setLoadingContent(true)
    setSrsMsg('')
    Promise.all([
      api.get(`/units/${selectedUnit.id}/lessons`),
      api.get(`/units/${selectedUnit.id}/vocabulary`),
    ]).then(([l, v]) => {
      setLessons(l.data)
      setVocab(v.data)
    }).finally(() => setLoadingContent(false))
  }, [selectedUnit])

  const addToSRS = async () => {
    try {
      const res = await api.post(`/me/srs/add-unit/${selectedUnit.id}`)
      setSrsMsg(`تمت إضافة ${res.data.added} بطاقة جديدة`)
    } catch { setSrsMsg('حدث خطأ') }
  }

  if (loadingUnits) return <CenteredSpinner size={32} height={260} />

  return (
    <div className="lessons-page" style={{ maxWidth: 1100, margin: '0 auto', padding: '28px 20px' }}>

      {openLesson && <LessonPanel lesson={openLesson} unitVocab={vocab} />}

      <div className="lessons-layout" style={{ display: 'flex', gap: 20 }}>
        <UnitPicker units={units} selectedId={selectedUnit?.id} onSelect={setSelectedUnit} />

        <div style={{ flex: 1, minWidth: 0 }}>
          {selectedUnit ? (
            <>
              <UnitHeader unit={selectedUnit} canSave={!!token} message={srsMsg} onAddToReview={addToSRS} />

              <div style={{ display: 'flex', gap: 0, borderBottom: '1px solid var(--border)', marginBottom: 20 }}>
                {PAGE_TABS.map(([key, label]) => (
                  <button
                    key={key}
                    onClick={() => setTab(key)}
                    className={tab === key ? 'tab-active' : 'tab-inactive'}
                    style={{
                      padding: '10px 18px', fontSize: 13, fontWeight: 500,
                      background: 'none', border: 'none', borderBottom: tab === key ? '2px solid var(--gold)' : '2px solid transparent',
                      cursor: 'pointer', fontFamily: 'DM Sans, sans-serif', transition: 'all .15s',
                      color: tab === key ? 'var(--navy)' : 'var(--muted)',
                    }}
                  >
                    {label}
                  </button>
                ))}
              </div>

              {loadingContent ? (
                <CenteredSpinner size={28} padding={40} />
              ) : tab === 'lessons' ? (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 12 }}>
                  {lessons.map(lesson => <LessonCard key={lesson.id} lesson={lesson} onOpen={setOpenLesson} />)}
                </div>
              ) : (
                <VocabularyList words={vocab} variant="page" />
              )}
            </>
          ) : (
            <div style={{ textAlign: 'center', color: 'var(--muted)', padding: '60px 0' }}>
              اختر وحدة من القائمة
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
