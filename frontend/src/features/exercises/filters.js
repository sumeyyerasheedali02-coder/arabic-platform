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
  word_order:      'ترتيب كلمات',
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
// content. The other filters follow Exercise.exercise_type, and only take
// exercises without a category, so every exercise belongs to exactly one filter
// (a word-order question is a fill_blank exercise, but not a "fill the blank").
const CATEGORY_FILTERS = new Set(['synonym', 'antonym', 'plural', 'comprehension', 'word_order'])
const TYPES_OF_FILTER = { translate_ar_tr: ['translate_ar_tr', 'translate_tr_ar'] }

export function matchesFilter(exercise, filter) {
  if (filter === 'all') return true
  if (CATEGORY_FILTERS.has(filter)) return exercise.category === filter
  return !exercise.category && (TYPES_OF_FILTER[filter] ?? [filter]).includes(exercise.exercise_type)
}
