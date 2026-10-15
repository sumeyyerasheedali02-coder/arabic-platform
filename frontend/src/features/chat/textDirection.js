// Prefer the paragraph's main script, so an Arabic vocabulary example does not
// reverse an otherwise Turkish explanation. Numbers and punctuation do not vote.
export function textDirection(text) {
  const arabic = (text.match(/\p{Script=Arabic}/gu) || []).length
  const latin = (text.match(/\p{Script=Latin}/gu) || []).length
  if (arabic === latin) return 'auto'
  return arabic > latin ? 'rtl' : 'ltr'
}
