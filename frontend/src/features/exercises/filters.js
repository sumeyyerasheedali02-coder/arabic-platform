// Labels for Exercise.exercise_type as stored by the backend.
export const TYPE_LABELS = {
  multiple_choice: 'اختيار من متعدد',
  fill_blank:      'اكمل الفراغ',
  translate_ar_tr: 'ترجمة عربي - تركي',
  translate_tr_ar: 'ترجمة تركي - عربي',
  true_false:      'صح ام خطا',
  form_sentence:   'كون جملة',
  respond:         'اجب بالعربية',
  match:           'وصل المعاني',
}

export const FILTER_OPTIONS = [
  { value: 'all',             label: 'الكل' },
  { value: 'multiple_choice', label: 'اختيار متعدد' },
  { value: 'fill_blank',      label: 'إكمال فراغ' },
  { value: 'true_false',      label: 'صح وخطأ' },
  { value: 'translate_ar_tr', label: 'ترجمة' },
  { value: 'match',           label: 'وصل' },
  { value: 'synonym',         label: 'مترادفات' },
  { value: 'antonym',         label: 'متعاكسات' },
  { value: 'plural',          label: 'الجمع' },
  { value: 'comprehension',   label: 'استيعاب قرائي' },
  { value: 'word_order',      label: 'ترتيب كلمات' },
]

export function matchesFilter(exercise, filter) {
  if (filter === 'all') return true
  if (filter === 'synonym')      return exercise.hint_ar === 'مترادف'
  if (filter === 'antonym')      return exercise.hint_ar === 'ضد / متعاكس'
  if (filter === 'plural')       return exercise.hint_ar === 'جمع الكلمة'
  if (filter === 'comprehension') return exercise.hint_ar === 'استيعاب قرائي'
  if (filter === 'word_order')   return exercise.question_ar && exercise.question_ar.includes('رَتِّب')
  return exercise.exercise_type === filter
}
