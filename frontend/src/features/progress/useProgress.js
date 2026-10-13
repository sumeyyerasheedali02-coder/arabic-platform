import { createContext, useContext } from 'react'

export const ProgressContext = createContext(null)

/**
 * The logged-in student's lesson progress (empty for guests).
 * { progress, loading, error, reload }  — call `reload` after saving progress.
 */
export const useProgress = () => useContext(ProgressContext)

export const completedLessons = (progress) => progress.filter(p => p.status === 'completed')
