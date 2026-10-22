import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { resolveDialogueAudio } from '../src/features/lessons/resolveDialogueAudio.js'
import { publishedDialogueAudio } from '../src/features/lessons/publishedDialogueAudio.js'

test('the compatibility catalogue uses the same immutable files as the backend catalogue', () => {
  const backend = readFileSync(new URL('../../files_extracted/content/dialogue_audio.py', import.meta.url), 'utf8')
  const files = new Map([...backend.matchAll(/\((\d+), (\d+)\): f"\{_BASE_URL\}\/([^"\n]+)"/g)]
    .map(([, unit, dialogue, file]) => [`${unit}:${dialogue}`, file]))
  assert.equal(Object.keys(publishedDialogueAudio).length, 50)
  for (const [key, media] of Object.entries(publishedDialogueAudio)) {
    assert.equal(media.url, `https://qyr8ctlxytrsnmot.public.blob.vercel-storage.com/${files.get(key)}`)
  }
})

test('previous API can play an approved recording using the course number', () => {
  const dialogue = { id: 9999, dialogue_number: 1, audio_url: null }
  assert.match(resolveDialogueAudio(dialogue, 11).url, /unit-11-dialogue-01-/)
  assert.deepEqual(resolveDialogueAudio(dialogue, 9999), {})
  assert.equal(dialogue.audio_url, null)
})

test('approved wording notices survive a previous API without the new field', () => {
  const media = resolveDialogueAudio({ dialogue_number: 1, audio_url: null }, 17)
  assert.match(media.url, /unit-17-dialogue-01-/)
  assert.equal(media.textDiffers, true)
  assert.equal(media.partial, false)
})

test('server recordings and their flags take priority over the compatibility catalogue', () => {
  assert.deepEqual(resolveDialogueAudio({ dialogue_number: 1,
    audio_url: 'https://example.test/replacement.mp3', audio_is_partial: true,
    audio_text_differs: false }, 17), {
    url: 'https://example.test/replacement.mp3', partial: true, textDiffers: false,
  })
})

test('unmatched listening texts and the last 16 units receive no fallback recording', () => {
  for (let unit = 17; unit <= 32; unit++) {
    assert.deepEqual(resolveDialogueAudio({ dialogue_number: 3 }, unit), {})
    assert.deepEqual(resolveDialogueAudio({ dialogue_number: 4 }, unit), {})
  }
  for (let unit = 33; unit <= 48; unit++) {
    assert.deepEqual(resolveDialogueAudio({ dialogue_number: 1 }, unit), {})
  }
})
