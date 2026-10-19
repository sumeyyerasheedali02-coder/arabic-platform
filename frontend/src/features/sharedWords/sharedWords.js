// Pure logic for the shared-vocabulary page: searching and counting.
// No React here, so it can be unit-tested on its own.

// Fold Arabic harakat/tatweel and letter variants, and Turkish case, so that a
// search matches regardless of vowels or how İ/ı are typed.
export function fold(text) {
  return (text || '')
    .replace(/[ً-ْٰـ]/g, '')
    .replace(/[أإآ]/g, 'ا')
    .replace(/ى/g, 'ي')
    .replace(/ة/g, 'ه')
    .replace(/İ/g, 'i').replace(/I/g, 'ı')
    .toLowerCase()
    .trim()
}

// Words of one category (or all) whose Arabic, Turkish or note contains the query.
export function filterWords(categories, categoryKey, query) {
  const needle = fold(query)
  const chosen = categoryKey === 'all'
    ? categories
    : categories.filter((c) => c.key === categoryKey)
  const words = chosen.flatMap((c) =>
    c.words.map((w) => ({ ...w, category: c.key, category_ar: c.title_ar })))
  if (!needle) return words
  return words.filter((w) =>
    fold(w.ar).includes(needle)
    || fold(w.tr).includes(needle)
    || fold(w.note).includes(needle))
}

export function totalCount(categories) {
  return categories.reduce((sum, c) => sum + c.words.length, 0)
}
