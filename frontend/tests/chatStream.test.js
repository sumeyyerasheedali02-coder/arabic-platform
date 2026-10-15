import test from 'node:test'
import assert from 'node:assert/strict'
// The parser has no dependency on browser state or API configuration.
import { readReply } from '../src/features/chat/readReply.js'

function bytesStream(text, size = 1) {
  const bytes = new TextEncoder().encode(text)
  return new ReadableStream({ start(controller) {
    for (let i = 0; i < bytes.length; i += size) controller.enqueue(bytes.slice(i, i + size))
    controller.close()
  } })
}

test('stream parser preserves Arabic across split UTF-8 bytes and lines', async () => {
  const chunks = []
  await readReply(bytesStream('{"text":"أهلًا"}\n{"text":" بك"}\n{"done":true}\n'), t => chunks.push(t))
  assert.equal(chunks.join(''), 'أهلًا بك')
})

test('a broken or failed stream is reported instead of appearing complete', async () => {
  await assert.rejects(readReply(bytesStream('{"text":"أهلًا"}\n'), () => {}), /انقطع/)
  await assert.rejects(readReply(bytesStream('{"error":"تأخر المساعد"}\n'), () => {}), /تأخر/)
})
