// Answer checking for guests, who practise without sending anything to the
// server. Keep in step with the backend rule in app/services/answers.py.

const PUNCTUATION = /[؟?!.,،;؛:«»"'’‘´`ʼ()[\]\-–—…]/g
const TURKISH_I = { 'İ': 'i', 'I': 'i', 'ı': 'i', '\u0307': '', 'â': 'a', 'Â': 'a', 'î': 'i', 'Î': 'i', 'û': 'u', 'Û': 'u' }
// A stored answer may list accepted alternatives: «Kırsal / Köy», «أجل / بلى».
const ALTERNATIVES_SEPARATOR = '/'
// The alef of a word, also after «ال» and its prefixes (وال، بال، كال، فال، لل): «الاخت» for «الأخت».
// An alef inside a word is kept: سال ≠ سأل.
const INITIAL_ALEF = /(?<![\p{L}\p{N}_])((?:[وفبكل]?ال|[وف]?لل)?)[أإٱ]/gu
// «علىكم» for «عليكم», «مراة» for «مرآة»; an alef with hamza inside a word is kept: سال ≠ سأل.
const LETTER_FOLD = { 'آ': 'ا', 'ى': 'ي' }
// «غرفه» for «غرفة»: only the ending of a word is compared alike.
const FINAL_TA_MARBUTA = /ة(?![\p{L}\p{N}_])/gu
// «مُهَنْدِسًا» is also written «مهندس»: the alef that carries a tanwin of fatha is optional.
const TANWIN_ALEF = /(?:ًا|اً)(?=[\s.,،؟?!؛;:»"')]|$)/g
const CHOICE_TYPES = ['multiple_choice', 'true_false', 'match']

/** Ignore vocalisation, alef/ya/ta marbuta spelling variants, punctuation and spacing, matching the server rule. */
export function normalizeAnswer(text) {
  return (text || '').normalize('NFC')
    .replace(/İ|I|ı|\u0307|â|Â|î|Î|û|Û/g, c => TURKISH_I[c])
    .split('').filter(c => !(c >= '\u064b' && c <= '\u065f') && c !== '\u0640' && c !== '\u0670')
    .join('')
    .replace(PUNCTUATION, ' ').replace(/\s+/g, ' ').trim()
    .toLowerCase()
    .replace(/[آى]/g, c => LETTER_FOLD[c])
    .replace(INITIAL_ALEF, '$1ا')
    .replace(FINAL_TA_MARBUTA, 'ه')
}

/** The whole stored answer and each alternative in it, normalised. */
export function acceptedAnswers(expected) {
  const forms = [expected || '', ...(expected || '').split(ALTERNATIVES_SEPARATOR)]
  return [...new Set(forms.map(normalizeAnswer))].filter(Boolean)
}

/** An exercise the student answers by typing, not by picking one of the options. */
export function isTypedExercise(exerciseType, options) {
  return !CHOICE_TYPES.includes(exerciseType) && !(options && options.length)
}

/** A single normalised word without «ال»; phrases are left alone. */
const withoutArticle = form => (!form.includes(' ') && form.startsWith('ال') && form.length > 3 ? form.slice(2) : form)

/** What a typed answer is compared by: without spaces («الحمدلله» = «الحمد لله») and, for a single word, with or without «ال». */
const typedKeys = form => [form.replace(/ /g, ''), withoutArticle(form)]

function tanwinFreeForms(expected) {
  const forms = [expected || '', ...(expected || '').split(ALTERNATIVES_SEPARATOR)]
  return forms.map(f => f.replace(TANWIN_ALEF, '')).filter(f => !forms.includes(f))
}

/**
 * `typed` exercises are compared more loosely: «قلم» for «القَلَم», «مهندس» for «مُهَنْدِسًا»,
 * «الحمدلله» for «الحمد لله». Picking an option never is.
 */
export function isCorrectAnswer(given, expected, typed = false) {
  const answer = normalizeAnswer(given)
  if (!answer) return false
  const accepted = acceptedAnswers(expected)
  if (accepted.includes(answer)) return true
  if (!typed) return false
  const loose = new Set([...accepted, ...tanwinFreeForms(expected).map(normalizeAnswer)].flatMap(typedKeys))
  return typedKeys(answer).some(key => loose.has(key))
}
