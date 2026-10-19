import assert from 'node:assert/strict'
import { test } from 'node:test'
import { fold, filterWords, totalCount } from '../src/features/sharedWords/sharedWords.js'

const CATEGORIES = [
  {
    key: 'religion', title_ar: 'الدين',
    words: [
      { ar: 'كِتَاب', tr: 'kitap', usage: 'شائعة', note: '' },
      { ar: 'رُؤْية', tr: 'rüya', usage: 'شائعة', note: 'حلم النوم في التركية' },
    ],
  },
  {
    key: 'home', title_ar: 'المنزل',
    words: [
      { ar: 'بَاب', tr: 'bab', usage: 'تراثية', note: 'باب البيت = kapı' },
    ],
  },
]

test('fold ignores harakat and folds Turkish İ/I', () => {
  assert.equal(fold('كِتَاب'), 'كتاب')
  assert.equal(fold('İSTANBUL'), 'istanbul')
  assert.equal(fold('IĞDIR'), 'ığdır')
})

test('all categories, no query, returns every word with its category', () => {
  const words = filterWords(CATEGORIES, 'all', '')
  assert.equal(words.length, 3)
  assert.equal(words[0].category, 'religion')
  assert.equal(words[0].category_ar, 'الدين')
})

test('a category key limits the words', () => {
  const words = filterWords(CATEGORIES, 'home', '')
  assert.equal(words.length, 1)
  assert.equal(words[0].tr, 'bab')
})

test('search matches Arabic ignoring harakat', () => {
  const words = filterWords(CATEGORIES, 'all', 'كتاب')
  assert.equal(words.length, 1)
  assert.equal(words[0].tr, 'kitap')
})

test('search matches the Turkish side and the note', () => {
  assert.equal(filterWords(CATEGORIES, 'all', 'rüya').length, 1)
  assert.equal(filterWords(CATEGORIES, 'all', 'حلم').length, 1)
  assert.equal(filterWords(CATEGORIES, 'all', 'kapı').length, 1)
})

test('no match gives an empty list', () => {
  assert.deepEqual(filterWords(CATEGORIES, 'all', 'سيارة'), [])
})

test('totalCount sums every category', () => {
  assert.equal(totalCount(CATEGORIES), 3)
})
