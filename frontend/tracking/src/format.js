export const format = value => value == null ? '—' : Number(value).toLocaleString(undefined, { maximumFractionDigits: 2 })
export function total(entry, keys) {
  return !entry || keys.some(key => entry[key] == null || entry[key] === '')
    ? null : keys.reduce((sum, key) => sum + Number(entry[key]), 0)
}
export const markValue = value => value === '' ? null : Number(value)
export const scoreClass = percent => percent >= 80 ? 'iyi' : percent >= 50 ? 'orta' : 'dusuk'

export function csvCell(value) {
  let text = String(value ?? '')
  // Names/notes can originate from users: neutralize spreadsheet formulas.
  if (/^[\s]*[=+\-@\t\r]/.test(text)) text = `'${text}`
  return `"${text.replace(/"/g, '""')}"`
}
export function downloadCsv(rows, filename) {
  const csv = '\uFEFF' + rows.map(row => row.map(csvCell).join(',')).join('\r\n')
  const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }))
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  anchor.click()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}
