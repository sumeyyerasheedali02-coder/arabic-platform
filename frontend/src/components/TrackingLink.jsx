import api from '../api/client'
import { useApiData } from '../api/useApiData'

export default function TrackingLink() {
  const development = import.meta.env.DEV
  const { data } = useApiData(development ? null : 'tracking-site', () =>
    api.get('/tracking/site').then(response => response.data))
  const destination = development ? 'http://localhost:5174/' : data?.site_url
  let href = null
  try {
    const url = new URL(destination)
    if (url.protocol === 'https:' || (development && url.protocol === 'http:')) href = url.href
  } catch { /* The link becomes available after the independent site has been configured. */ }
  return href ? <a className="tracking-link" href={href} title="فتح منصة العلامات المستقلة">منصة العلامات ↗</a> : null
}
