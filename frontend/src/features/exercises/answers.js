// Answer checking for guests, who practise without sending anything to the
// server. Keep in step with the backend rule in app/services/answers.py.

const PUNCTUATION = /[؟?!.,،;؛:«»"'()[\]\-–—…]/g
const TURKISH_I = { 'İ': 'i', 'I': 'i', 'ı': 'i', '\u0307': '', 'â': 'a', 'Â': 'a', 'î': 'i', 'Î': 'i', 'û': 'u', 'Û': 'u' }
// A stored answer may list accepted alternatives: «Kırsal / Köy», «أجل / بلى».
const ALTERNATIVES_SEPARATOR = '/'

/** Ignore vocalisation, initial alef variants, punctuation and spacing, matching the server rule. */
export function normalizeAnswer(text) {
  return (text || '').normalize('NFC')
    .replace(/İ|I|ı|\u0307|â|Â|î|Î|û|Û/g, c => TURKISH_I[c])
    .split('').filter(c => !(c >= '\u064b' && c <= '\u065f') && c !== '\u0640' && c !== '\u0670')
    .join('')
    .replace(PUNCTUATION, ' ').replace(/\s+/g, ' ').trim()
    .toLowerCase()
    .replace(/(?<![\p{L}\p{N}_])[أإآٱ]/gu, 'ا')
}

/** The whole stored answer and each alternative in it, normalised. */
export function acceptedAnswers(expected) {
  const forms = [expected || '', ...(expected || '').split(ALTERNATIVES_SEPARATOR)]
  return [...new Set(forms.map(normalizeAnswer))].filter(Boolean)
}

export function isCorrectAnswer(given, expected) {
  const answer = normalizeAnswer(given)
  return Boolean(answer) && acceptedAnswers(expected).includes(answer)
}
