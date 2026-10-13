export function normalizeStudentNumber(value) {
  return value.trim().replace(/[٠-٩۰-۹]/g, digit => {
    const code = digit.charCodeAt(0)
    return String(code >= 0x6f0 ? code - 0x6f0 : code - 0x660)
  })
}

export const isStudentNumber = value => /^[0-9]{1,32}$/.test(normalizeStudentNumber(value))
