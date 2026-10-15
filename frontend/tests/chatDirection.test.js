import test from 'node:test'
import assert from 'node:assert/strict'
import { textDirection } from '../src/features/chat/textDirection.js'

test('Turkish explanations remain LTR with punctuation and Arabic examples', () => {
  assert.equal(textDirection('Merhaba! Nasılsın?'), 'ltr')
  assert.equal(textDirection('"كتاب" Türkçede kitap demektir.'), 'ltr')
  assert.equal(textDirection('123. Örnek: Ben öğrenciyim.'), 'ltr')
})

test('Arabic explanations remain RTL with Turkish examples', () => {
  assert.equal(textDirection('مرحبًا! كيف حالك؟'), 'rtl')
  assert.equal(textDirection('Kitap تعني كتابًا باللغة العربية.'), 'rtl')
  assert.equal(textDirection('123 ...'), 'auto')
})
