import { publishedDialogueAudio } from './publishedDialogueAudio.js'

/** Resolve verified CDN media by content numbers, never database IDs. */
export function resolveDialogueAudio(dialogue, unitNumber) {
  if (dialogue.audio_url) {
    return {
      url: dialogue.audio_url,
      partial: Boolean(dialogue.audio_is_partial),
      textDiffers: Boolean(dialogue.audio_text_differs),
    }
  }
  return publishedDialogueAudio[`${unitNumber}:${dialogue.dialogue_number}`] ?? {}
}
