import { useSyncExternalStore } from 'react'

const phone = window.matchMedia('(max-width: 768px)')
const subscribe = callback => {
  phone.addEventListener('change', callback)
  return () => phone.removeEventListener('change', callback)
}
export function usePhoneLayout() {
  return useSyncExternalStore(subscribe, () => phone.matches, () => false)
}
