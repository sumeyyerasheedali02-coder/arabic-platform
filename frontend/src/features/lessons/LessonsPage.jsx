import { useState } from 'react'
import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import { useAuth } from '../../auth/useAuth'
import ErrorState from '../../components/ErrorState'
import { CenteredSpinner } from '../../components/Spinner'
import { useUnits } from '../units/useUnits'
import LessonCard from './LessonCard'
import LessonPanel from './LessonPanel'
import UnitHeader from './UnitHeader'
import UnitPicker from './UnitPicker'
import { VocabularyList } from './VocabularyRow'

const PAGE_TABS = [['lessons', 'الدروس'], ['vocab', 'المفردات']]

const loadUnitContent = (unitId) => Promise.all([
  api.get(`/units/${unitId}/lessons`),
  api.get(`/units/${unitId}/vocabulary`),
]).then(([lessons, vocab]) => ({ lessons: lessons.data, vocab: vocab.data }))

export default function LessonsPage() {
  const { token } = useAuth()
  const { units, selectedUnit, selectUnit, loading: loadingUnits, error: unitsError, reload: reloadUnits } = useUnits()
  const unitId = selectedUnit?.id
  const content = useApiData(unitId == null ? null : `unit-content:${unitId}`, () => loadUnitContent(unitId))

  const [tab, setTab]                   = useState('lessons')
  const [srsMsg, setSrsMsg]             = useState({ unitId: null, text: '' })
  const [openLessonId, setOpenLessonId] = useState(null)

  const lessons = content.data?.lessons ?? []
  const vocab   = content.data?.vocab ?? []
  // Only a lesson of the unit on screen can be open
  const openLesson = lessons.find(lesson => lesson.id === openLessonId) ?? null

  const addToSRS = async () => {
    try {
      const res = await api.post(`/me/srs/add-unit/${unitId}`)
      setSrsMsg({ unitId, text: `تمت إضافة ${res.data.added} بطاقة جديدة` })
    } catch { setSrsMsg({ unitId, text: 'حدث خطأ' }) }
  }

  if (loadingUnits) return <CenteredSpinner size={32} height={260} />
  if (unitsError && units.length === 0) return <ErrorState onRetry={reloadUnits} />

  return (
    <div className="lessons-page" style={{ maxWidth: 1100, margin: '0 auto', padding: '28px 20px' }}>

      {openLesson && (
        <LessonPanel key={openLesson.id} lesson={openLesson} unitVocab={vocab} onClose={() => setOpenLessonId(null)} />
      )}

      <div className="lessons-layout" style={{ display: 'flex', gap: 20 }}>
        <UnitPicker units={units} selectedId={unitId} onSelect={selectUnit} />

        <div style={{ flex: 1, minWidth: 0 }}>
          {selectedUnit ? (
            <>
              <UnitHeader
                unit={selectedUnit} canSave={!!token}
                message={srsMsg.unitId === unitId ? srsMsg.text : ''}
                onAddToReview={addToSRS}
              />

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

              {content.loading ? (
                <CenteredSpinner size={28} padding={40} />
              ) : content.error ? (
                <ErrorState compact onRetry={content.reload} />
              ) : tab === 'lessons' ? (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 12 }}>
                  {lessons.map(lesson => <LessonCard key={lesson.id} lesson={lesson} onOpen={l => setOpenLessonId(l.id)} />)}
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
