// Answer checking for guests, who practise without sending anything to the
// server. Keep in step with the backend rule in app/services/answers.py.

/** Ignore vocalisation and initial alef variants, matching the server rule. */
export function normalizeAnswer(text) {
  return (text || '').normalize('NFC').trim().toLowerCase()
    .split('').filter(c => !(c >= '\u064b' && c <= '\u065f') && c !== '\u0640' && c !== '\u0670')
    .join('').trim()
    .replace(/(?<![\p{L}\p{N}_])[أإآٱ]/gu, 'ا')
}

export function isCorrectAnswer(given, expected) {
  return normalizeAnswer(given) === normalizeAnswer(expected)
}
