export const staffHome = account => account?.is_admin ? '/admin' : '/teacher'
export const studentPath = (account, id) => `${account?.is_admin ? '/admin' : '/teacher'}/students/${id}`

export const staffLinks = admin => admin ? [
  { to: '/admin', label: 'نظرة عامة', exact: true },
  { to: '/admin/teachers', label: 'المدرسون' },
  { to: '/admin/sections', label: 'الشُّعَب' },
  { to: '/admin/students', label: 'الطلاب والمتابعة' },
  { to: '/content', label: 'المحتوى التعليمي' },
  { to: '/admin/audit', label: 'سجل الإدارة' },
  { to: '/account', label: 'إعدادات الحساب' },
] : [
  { to: '/teacher', label: 'نظرة عامة', exact: true },
  { to: '/teacher/students', label: 'طلابي' },
  { to: '/content', label: 'المحتوى التعليمي' },
  { to: '/account', label: 'إعدادات الحساب' },
]

export function staffPageTitle(path, admin) {
  return staffLinks(admin).find(link =>
    link.exact ? path === link.to : path.startsWith(link.to))?.label ?? 'المحتوى التعليمي'
}
