import { API_BASE_URL } from '../../api/config'
import { storedToken } from '../../auth/session'
import { readReply } from './readReply'

export async function streamReply(messages, onText, signal) {
  // Optional: a logged-in student gets their own message allowance instead of
  // sharing the guest allowance of their network address.
  const token = storedToken()
  const response = await fetch(`${API_BASE_URL}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
    body: JSON.stringify({ messages: messages.slice(-8) }), signal,
  })
  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    throw new Error(typeof data.detail === 'string' ? data.detail : 'المساعد غير متاح حاليًا. حاول مجددًا.')
  }
  if (!response.body) throw new Error('تعذّر استقبال الرد. حاول مجددًا.')
  await readReply(response.body, onText)
}
