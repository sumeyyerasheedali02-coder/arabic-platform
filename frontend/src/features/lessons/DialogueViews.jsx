import DialogueAudio from './DialogueAudio'
import { resolveDialogueAudio } from './resolveDialogueAudio'

const AMIRI = "'Amiri', serif"

// A line without a speaker is narration: a stage direction inside a dialogue,
// or a paragraph of a listening text (Book 3 has texts instead of dialogues).
const isNarration = (line) => !line.speaker

function Narration({ line }) {
  return (
    <div>
      <div style={{ fontFamily: AMIRI, fontSize: 16, color: 'var(--text)', lineHeight: 1.9 }}>
        {line.text_ar}
      </div>
      {line.translation_tr && (
        <div style={{ fontSize: 11, color: 'var(--muted)', marginTop: 2 }} dir="ltr">
          {line.translation_tr}
        </div>
      )}
    </div>
  )
}

/** Dialogues as a script: speaker name beside each line ("الدروس" tab). */
function PublishedAudio({ dialogue, unitNumber }) {
  const media = resolveDialogueAudio(dialogue, unitNumber)
  return <DialogueAudio key={media.url} {...media} title={dialogue.title_ar} />
}

export function DialogueScript({ dialogues, unitNumber }) {
  return dialogues.map(dialogue => (
    <div key={dialogue.id} style={{ marginBottom: 24 }}>
      {dialogue.title_ar && (
        <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--navy)', marginBottom: 4 }}>
          {dialogue.title_ar}
        </div>
      )}
      {dialogue.situation_tr && (
        <div style={{ fontSize: 11, color: 'var(--muted)', fontStyle: 'italic', marginBottom: 12 }} dir="ltr">
          {dialogue.situation_tr}
        </div>
      )}
      <PublishedAudio dialogue={dialogue} unitNumber={unitNumber} />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {dialogue.lines?.map((line, i) => isNarration(line) ? <Narration key={i} line={line} /> : (
          <div key={i} style={{
            display: 'flex', gap: 10, alignItems: 'flex-start',
            opacity: line.is_key_phrase ? 1 : 0.65,
          }}>
            <span style={{
              fontSize: 11, fontWeight: 600, color: 'var(--gold)',
              minWidth: 80, flexShrink: 0, paddingTop: 2, fontFamily: AMIRI,
            }}>
              {line.speaker}
            </span>
            <div style={{ flex: 1 }}>
              <div style={{
                fontFamily: AMIRI, fontSize: 16,
                color: line.is_key_phrase ? 'var(--navy)' : 'var(--text)',
                fontWeight: line.is_key_phrase ? 700 : 400,
                lineHeight: 1.6,
              }}>
                {line.text_ar}
              </div>
              {line.translation_tr && (
                <div style={{ fontSize: 11, color: 'var(--muted)', marginTop: 2 }} dir="ltr">
                  {line.translation_tr}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  ))
}

/** Dialogues as alternating chat bubbles ("الحوار" tab). */
export function DialogueBubbles({ dialogues, unitNumber }) {
  return dialogues.map(dialogue => (
    <div key={dialogue.id} style={{ marginBottom: 28 }}>
      {dialogue.title_ar && (
        <div style={{
          fontSize: 14, fontWeight: 600, color: 'var(--navy)',
          fontFamily: AMIRI, marginBottom: 6,
        }}>
          {dialogue.title_ar}
        </div>
      )}
      {dialogue.situation_tr && (
        <div style={{
          fontSize: 11, color: 'var(--muted)', fontStyle: 'italic',
          marginBottom: 14, padding: '6px 12px',
          background: 'var(--cream)', border: '1px solid var(--border)',
          borderRadius: 8,
        }} dir="ltr">
          📍 {dialogue.situation_tr}
        </div>
      )}

      <PublishedAudio dialogue={dialogue} unitNumber={unitNumber} />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {dialogue.lines?.map((line, i) => {
          if (isNarration(line)) return <Narration key={i} line={line} />
          // Alternate sides between spoken lines only, so narration does not flip them.
          const spoken = dialogue.lines.slice(0, i).filter(l => !isNarration(l)).length
          const isRight = spoken % 2 === 0
          return (
            <div key={i} style={{
              display: 'flex', flexDirection: isRight ? 'row' : 'row-reverse',
              alignItems: 'flex-end', gap: 8,
            }}>
              <div style={{
                width: 30, height: 30, borderRadius: '50%', flexShrink: 0,
                background: isRight ? 'var(--navy)' : '#185FA5',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 11, fontWeight: 700, color: '#fff',
                fontFamily: AMIRI,
              }}>
                {line.speaker?.[0] || '؟'}
              </div>
              <div style={{
                background: isRight ? 'var(--cream)' : 'var(--navy)',
                border: `1px solid ${isRight ? 'var(--border)' : 'var(--navy)'}`,
                borderRadius: isRight ? '4px 12px 12px 12px' : '12px 4px 12px 12px',
                padding: '10px 14px', maxWidth: '75%',
              }}>
                <div style={{
                  fontFamily: AMIRI, fontSize: 15,
                  color: isRight ? 'var(--navy)' : '#fff',
                  lineHeight: 1.6, direction: 'rtl',
                  fontWeight: line.is_key_phrase ? 700 : 400,
                }}>
                  {line.text_ar}
                </div>
                {line.translation_tr && (
                  <div style={{ fontSize: 11, color: isRight ? 'var(--muted)' : 'rgba(255,255,255,.55)', marginTop: 3 }} dir="ltr">
                    {line.translation_tr}
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  ))
}
