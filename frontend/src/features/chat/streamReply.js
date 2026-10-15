import { API_BASE_URL } from '../../api/config'
import { readReply } from './readReply'

export async function streamReply(messages, onText, signal) {
  const response = await fetch(`${API_BASE_URL}/chat/stream`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages: messages.slice(-8) }), signal,
  })
  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    throw new Error(typeof data.detail === 'string' ? data.detail : 'المساعد غير متاح حاليًا. حاول مجددًا.')
  }
  if (!response.body) throw new Error('تعذّر استقبال الرد. حاول مجددًا.')
  await readReply(response.body, onText)
}
