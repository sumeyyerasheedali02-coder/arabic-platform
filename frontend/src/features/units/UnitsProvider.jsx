import { useCallback, useMemo, useState } from 'react'
import api from '../../api/client'
import { useApiData } from '../../api/useApiData'
import { UnitsContext } from './useUnits'

const STORAGE_KEY = 'selectedUnitId'
const NO_UNITS = []

// The choice survives a page reload, but only for this browser tab.
function rememberedUnitId() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    return raw == null ? null : Number(raw)
  } catch {
    return null
  }
}

export function UnitsProvider({ children, active = true }) {
  const { data, loading, error, reload } = useApiData(active ? 'units' : null, () => api.get('/units').then(r => r.data))
  const [selectedId, setSelectedId] = useState(rememberedUnitId)

  const units = data ?? NO_UNITS
  // Fall back to the first unit when nothing (or something no longer there) is selected
  const selectedUnit = units.find(u => u.id === selectedId) ?? units[0] ?? null

  const selectUnit = useCallback((unit) => {
    const id = unit?.id ?? null
    setSelectedId(id)
    try {
      if (id == null) sessionStorage.removeItem(STORAGE_KEY)
      else sessionStorage.setItem(STORAGE_KEY, String(id))
    } catch { /* storage unavailable: the choice simply lasts until reload */ }
  }, [])

  const value = useMemo(
    () => ({ units, loading, error, reload, selectedUnit, selectUnit }),
    [units, loading, error, reload, selectedUnit, selectUnit],
  )
  return <UnitsContext.Provider value={value}>{children}</UnitsContext.Provider>
}
