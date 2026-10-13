// Lesson kinds as stored in Lesson.lesson_type by the backend.
export const TYPE_LABEL = {
  hiwar: 'حوار', mufradat: 'مفردات', nahw: 'نحو',
  tadrib: 'تدريب', aswat: 'أصوات',
}

export const TYPE_DOT = {
  hiwar:    '#185FA5',
  mufradat: '#1D9E75',
  nahw:     '#3C3489',
  tadrib:   '#854F0B',
  aswat:    '#712B13',
}

export const lessonColor = (lesson) => TYPE_DOT[lesson.lesson_type] || '#6b7280'
export const lessonLabel = (lesson) => TYPE_LABEL[lesson.lesson_type] || lesson.lesson_type
