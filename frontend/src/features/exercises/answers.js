// Answer checking for guests, who practise without sending anything to the
// server. Keep in step with the backend rule in app/services/answers.py.

/** Drop Arabic diacritics (U+064B–U+065F) and tatweel, outer spaces and letter case. */
export function normalizeAnswer(text) {
  return (text || '').trim().toLowerCase()
    .split('').filter(c => !(c >= '\u064b' && c <= '\u065f') && c !== '\u0640').join('').trim()
}

export function isCorrectAnswer(given, expected) {
  return normalizeAnswer(given) === normalizeAnswer(expected)
}
