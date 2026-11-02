import { useEffect } from 'react'

/** Keep keyboard/screen-reader navigation inside an open overlay and restore it on close. */
export function useOverlayFocus(ref, active, onClose, backgroundSelector) {
  useEffect(() => {
    const panel = ref.current
    if (!active || !panel) return
    const previous = document.activeElement
    const background = [...document.querySelectorAll(backgroundSelector)]
      .map(element => ({ element, inert: element.inert }))
    background.forEach(({ element }) => { element.inert = true })
    const focusable = () => [...panel.querySelectorAll('button, a[href], input, select, textarea, [tabindex]')]
      .filter(element => !element.disabled && element.tabIndex >= 0 && element.getClientRects().length)
    ;(focusable()[0] ?? panel).focus({ preventScroll: true })
    const handleKey = event => {
      if (event.key === 'Escape') {
        event.preventDefault()
        onClose()
      }
      if (event.key !== 'Tab') return
      const elements = focusable()
      const first = elements[0] ?? panel
      const last = elements.at(-1) ?? panel
      if (event.shiftKey && (document.activeElement === first || document.activeElement === panel)) {
        event.preventDefault()
        last.focus()
      } else if (!event.shiftKey && (document.activeElement === last || !panel.contains(document.activeElement))) {
        event.preventDefault()
        first.focus()
      }
    }
    document.addEventListener('keydown', handleKey)
    return () => {
      document.removeEventListener('keydown', handleKey)
      background.forEach(({ element, inert }) => { element.inert = inert })
      if (previous?.isConnected) previous.focus({ preventScroll: true })
    }
  }, [ref, active, onClose, backgroundSelector])
}
