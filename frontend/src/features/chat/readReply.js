// NDJSON lines may be split anywhere, including inside a UTF-8 Arabic letter.
export async function readReply(body, onText) {
  const reader = body.getReader()
  const decoder = new TextDecoder()
  let pending = ''
  let done = false
  function consume(line) {
    if (!line.trim()) return
    const event = JSON.parse(line)
    if (event.error) throw new Error(event.error)
    if (event.text) onText(event.text)
    if (event.done) done = true
  }
  try {
    while (true) {
      const next = await reader.read()
      pending += decoder.decode(next.value, { stream: !next.done })
      const lines = pending.split('\n')
      pending = lines.pop()
      lines.forEach(consume)
      if (next.done) break
    }
    if (pending.trim()) consume(pending)
    if (!done) throw new Error('انقطع الرد قبل اكتماله. حاول مجددًا.')
  } finally {
    await reader.cancel().catch(() => {})
    reader.releaseLock()
  }
}

