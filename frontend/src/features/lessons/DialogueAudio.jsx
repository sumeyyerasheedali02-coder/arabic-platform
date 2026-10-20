import { useState } from 'react'

export default function DialogueAudio({ url, title, partial = false, textDiffers = false }) {
  const [failed, setFailed] = useState(false)
  if (!url) return null

  function handlePlay(event) {
    setFailed(false)
    for (const audio of document.querySelectorAll('audio[data-dialogue-audio]')) {
      if (audio !== event.currentTarget) audio.pause()
    }
  }

  return (
    <div style={{ margin: '12px 0 16px' }}>
      {partial && (
        <p style={{ fontSize: 12, color: 'var(--muted)', margin: '0 0 6px' }}>
          تسجيل جزئي — يغطي بداية الحوار فقط.
        </p>
      )}
      {textDiffers && (
        <p style={{ fontSize: 12, color: 'var(--muted)', margin: '0 0 6px' }}>
          تنبيه: تختلف بعض عبارات التسجيل عن النص المكتوب.
        </p>
      )}
      <audio
        data-dialogue-audio
        controls
        preload="none"
        src={url}
        aria-label={`استمع إلى ${title || 'الحوار'}`}
        onPlay={handlePlay}
        onError={() => setFailed(true)}
        onLoadedData={() => setFailed(false)}
        style={{ display: 'block', width: '100%', maxWidth: 520 }}
      />
      {failed && (
        <p role="status" style={{ fontSize: 12, color: 'var(--muted)', margin: '6px 0' }}>
          تعذّر تشغيل الصوت. حاول مجددًا بعد التحقق من الاتصال.
        </p>
      )}
    </div>
  )
}
