const utcDate = value => new Date(/Z$|[+-]\d\d:\d\d$/.test(value) ? value : value + 'Z')

export const formatDate = value => value
  ? utcDate(value).toLocaleDateString('ar', {
    day: 'numeric', month: 'short', year: 'numeric',
  }) : '—'

export const formatDateTime = value => value ? utcDate(value).toLocaleString('ar', {
  day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit',
}) : '—'

export function apiError(error) {
  const detail = error.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (error.response?.status === 403) return 'ليس لديك صلاحية لهذه العملية.'
  if (error.response?.status === 404) return 'السجل غير موجود أو غير متاح لحسابك.'
  return 'تعذر إتمام العملية. تحقق من الاتصال وحاول مجددًا.'
}
