import { useEffect } from 'react'

export function useLessonActivity(lessonId) {
  useEffect(() => {
    if (!lessonId) return
    window.dispatchEvent(new CustomEvent('arabiq:active-lesson', { detail: Number(lessonId) }))
    return () => window.dispatchEvent(new CustomEvent('arabiq:active-lesson', { detail: null }))
  }, [lessonId])
}
