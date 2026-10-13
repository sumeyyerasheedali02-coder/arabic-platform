// Texts of the login page in its two languages (the rest of the app is Arabic only).
export const LOGIN_TEXTS = {
  ar: {
    title: 'تسجيل الدخول',
    subtitle: 'مرحباً بعودتك، أكمل رحلتك التعليمية',
    email: 'البريد الإلكتروني',
    password: 'كلمة المرور',
    name: 'الاسم الكامل',
    year: 'السنة الدراسية',
    login: 'تسجيل الدخول',
    signup: 'إنشاء الحساب',
    next: 'متابعة',
    invalidEmail: 'أدخل بريداً إلكترونياً صحيحاً',
    guest: 'تصفّح كزائر',
    back: '← العودة',
    checking: 'جارٍ التحقق...',
    newAccount: 'حساب جديد',
    newSub: 'أكمل بياناتك',
    hint: 'أدخل بريدك الإلكتروني ثم اضغط «متابعة»',
    loading: 'جارٍ التحميل...',
    welcome: 'مرحباً بعودتك!',
    enterPwd: 'أدخل كلمة المرور',
    footer: 'جامعة كارابوك — كلية الإلهيات',
  },
  tr: {
    title: 'Giriş Yap',
    subtitle: 'Tekrar hoş geldin, öğrenme yolculuğuna devam et',
    email: 'E-posta',
    password: 'Şifre',
    name: 'Ad Soyad',
    year: 'Sınıf',
    login: 'Giriş Yap',
    signup: 'Yeni hesap oluştur',
    next: 'Devam et',
    invalidEmail: 'Geçerli bir e-posta adresi girin',
    guest: 'Misafir olarak gözat',
    back: '← Geri',
    checking: 'Kontrol ediliyor...',
    newAccount: 'Yeni Hesap',
    newSub: 'Bilgilerinizi tamamlayın',
    hint: 'E-postanızı girin ve «Devam et» düğmesine basın',
    loading: 'Yükleniyor...',
    welcome: 'Tekrar hoş geldin!',
    enterPwd: 'Şifrenizi girin',
    footer: 'Karabük Üniversitesi — İlahiyat Fakültesi',
  },
}

// "أدخل كلمة مرور من 6 أحرف على الأقل"
export const PASSWORD_TOO_SHORT = 'أدخل كلمة مرور من 6 أحرف على الأقل'
// "تأكد من البريد وكلمة المرور (6 أحرف على الأقل)"
export const LOGIN_FAILED = 'تأكد من البريد وكلمة المرور (6 أحرف على الأقل)'

export const MIN_PASSWORD_LENGTH = 6
export const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
