import { createContext, useContext } from 'react'

export const UnitsContext = createContext(null)

/**
 * The course units and the one the student is working on.
 * { units, loading, error, reload, selectedUnit, selectUnit(unit) }
 *
 * `selectedUnit` is the single source of truth for "the current unit": the
 * sidebar, the lessons page, the exercises page and the dashboard cards all
 * read and change it here.
 */
export const useUnits = () => useContext(UnitsContext)
