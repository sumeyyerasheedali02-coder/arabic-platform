import { useApiData } from '../../api/useApiData'

export function useStaffApiData(key, load) {
  return useApiData(key, load, { refreshOnFocus: true })
}
