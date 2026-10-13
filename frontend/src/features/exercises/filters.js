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
  synonym:         'مترادفات',
  antonym:         'متعاكسات',
  plural:          'الجمع',
  comprehension:   'استيعاب قرائي',
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

// Filters that follow Exercise.category, which the server derives from the
// content. The other filters follow Exercise.exercise_type.
const CATEGORY_FILTERS = new Set(['synonym', 'antonym', 'plural', 'comprehension', 'word_order'])

export function matchesFilter(exercise, filter) {
  if (filter === 'all') return true
  if (CATEGORY_FILTERS.has(filter)) return exercise.category === filter
  return exercise.exercise_type === filter
}
