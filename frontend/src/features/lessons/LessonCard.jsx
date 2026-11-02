import { lessonColor, lessonLabel } from './lessonTypes'

function CardIcon({ exercise, grammar }) {
  return (
    <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      {exercise ? <><rect x="5" y="4" width="14" height="17" rx="2" /><path d="M9 4V2h6v2M9 10l1 1 2-2M14 10h2M9 16l1 1 2-2M14 16h2" /></>
        : grammar ? <><rect x="2" y="3" width="6" height="6" rx="1" fill="currentColor" stroke="none" /><rect x="16" y="15" width="6" height="6" rx="1" fill="currentColor" stroke="none" /><path d="M5 12v6h7M11 6h8v6" /></>
          : <><path d="M14 15H8l-4 3v-5a6 6 0 1 1 10 2Z" fill="currentColor" fillOpacity=".85" /><path d="M15 9a5 5 0 0 1 5 8v4l-4-2h-3" /></>}
    </svg>
  )
}

/** Lesson entry, or the unit practice entry replacing its duplicate vocabulary card. */
export default function LessonCard({ lesson, onOpen, exercise = false, unitNumber, progress, progressAvailable = false }) {
  const color = exercise ? '#278664' : lessonColor(lesson)
  const isComplete = !exercise && progressAvailable && progress?.status === 'completed'
  const isStarted = !exercise && progressAvailable && !isComplete && progress?.status === 'in_progress'
  const percent = !exercise && progressAvailable && !isStarted ? (isComplete ? 100 : 0) : null
  const status = isComplete ? 'مكتمل' : isStarted ? 'قيد التقدّم' : progressAvailable && !exercise ? 'لم يبدأ' : null
  const rules = lesson.grammar_focus?.split('|').map(rule => rule.trim()).filter(Boolean) ?? []
  const detail = exercise ? 'تدريب على دروس الوحدة' : lesson.lesson_type === 'nahw'
    ? rules.length === 1 ? 'قاعدة نحوية واحدة' : rules.length === 2 ? 'قاعدتان نحويتان' : rules.length ? `${rules.length} قواعد نحوية` : 'شرح القواعد والتراكيب'
    : lesson.lesson_type === 'hiwar' ? 'قراءة الحوارات والاستماع' : 'محتوى الدرس'

  return (
    <button className={`lesson-entry-card${exercise ? ' lesson-entry-practice' : ''}`} style={{ '--lesson-color': color, '--lesson-tint': `${color}16` }} onClick={() => onOpen(lesson)}>
      <div className="lesson-entry-top">
        <span className="lesson-entry-icon"><CardIcon exercise={exercise} grammar={lesson.lesson_type === 'nahw'} /></span>
        <span className="lesson-entry-kicker">{exercise ? `تدريب · الوحدة ${unitNumber}` : lessonLabel(lesson)}</span>
        <span className="lesson-entry-sequence" dir="ltr" aria-hidden="true">{String(lesson.lesson_number).padStart(2, '0')}</span>
      </div>
      <div className="lesson-entry-titles">
        <h2>{exercise ? 'تمرينات الوحدة' : lesson.title_ar}</h2>
        {(exercise || lesson.title_tr) && <p lang="tr" dir="ltr">{exercise ? 'Ünite alıştırmaları' : lesson.title_tr}</p>}
      </div>
      <p className="lesson-entry-detail">{detail}</p>
      <div className="lesson-entry-footer">
        <span className="lesson-entry-action">{exercise ? 'ابدأ التدريب' : isStarted ? 'أكمل الدرس' : isComplete ? 'راجع الدرس' : 'افتح الدرس'}</span>
        {status && <span className="lesson-entry-status">{isComplete && <span aria-hidden="true">✓</span>}{status}{percent !== null && <span dir="ltr">{percent}%</span>}</span>}
        <span className="lesson-entry-arrow" aria-hidden="true">←</span>
      </div>
      {percent !== null && <span className="lesson-entry-track" aria-hidden="true"><span style={{ width: `${percent}%` }} /></span>}
    </button>
  )
}
