import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ══════════════════════════════════════════
# 1. إصلاح الشعار المتحرك في Landing.jsx
# ══════════════════════════════════════════
LANDING_PATH = r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages\Landing.jsx"
landing = open(LANDING_PATH, encoding="utf-8").read()

# إضافة keyframes مباشرة في style tag الموجود
old_style = "<style>{`"
new_style = """<style>{`
        @keyframes aq-float-slow {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-10px); }
        }"""
if "aq-float-slow" not in landing.split("<style>")[1] if "<style>" in landing else "":
    landing = landing.replace(old_style, new_style)
    print("  ✓ أُضيف keyframe التحريك في Landing")

open(LANDING_PATH, "w", encoding="utf-8").write(landing)
print("✓ 1. إصلاح الشعار المتحرك")

# ══════════════════════════════════════════
# 2. إضافة مبدل اللغة في LoginRegister.jsx
# ══════════════════════════════════════════
LOGIN_PATH = r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages\LoginRegister.jsx"
login = open(LOGIN_PATH, encoding="utf-8").read()

if "langSw" not in login:
    # أضف state للغة بعد useState الأخير
    old_state = "const [submitting, setSubmitting] = useState(false)"
    new_state = """const [submitting, setSubmitting] = useState(false)
  const [lang, setLang] = useState('ar')"""
    login = login.replace(old_state, new_state)

    # أضف ترجمات بعد تعريف المتغيرات
    old_nav = "const navigate                  = useNavigate()"
    new_nav = """const navigate                  = useNavigate()

  const langText = {
    ar: {
      title: '\u062a\u0633\u062c\u064a\u0644 \u0627\u0644\u062f\u062e\u0648\u0644',
      subtitle: '\u0645\u0631\u062d\u0628\u0627\u064b \u0628\u0639\u0648\u062f\u062a\u0643\u060c \u0623\u0643\u0645\u0644 \u0631\u062d\u0644\u062a\u0643 \u0627\u0644\u062a\u0639\u0644\u064a\u0645\u064a\u0629',
      email: '\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a',
      password: '\u0643\u0644\u0645\u0629 \u0627\u0644\u0645\u0631\u0648\u0631',
      name: '\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0643\u0627\u0645\u0644',
      year: '\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u062f\u0631\u0627\u0633\u064a\u0629',
      login: '\u062a\u0633\u062c\u064a\u0644 \u0627\u0644\u062f\u062e\u0648\u0644',
      signup: '\u0625\u0646\u0634\u0627\u0621 \u0627\u0644\u062d\u0633\u0627\u0628',
      guest: '\u062a\u0635\u0641\u0651\u062d \u0643\u0636\u064a\u0641 \u0628\u062f\u0648\u0646 \u062a\u0633\u062c\u064a\u0644',
      back: '\u2190 \u0627\u0644\u0639\u0648\u062f\u0629',
      checking: '\u062c\u0627\u0631\u064d \u0627\u0644\u062a\u062d\u0642\u0642...',
      newAccount: '\u062d\u0633\u0627\u0628 \u062c\u062f\u064a\u062f',
      newSub: '\u0623\u0643\u0645\u0644 \u0628\u064a\u0627\u0646\u0627\u062a\u0643 \u0644\u0628\u062f\u0621 \u0631\u062d\u0644\u0629 \u0627\u0644\u062a\u0639\u0644\u0651\u0645',
      hint: '\u0623\u062f\u062e\u0644 \u0628\u0631\u064a\u062f\u0643 \u0648\u0627\u0636\u063a\u0637 Tab \u0623\u0648 Enter \u0644\u0644\u0645\u062a\u0627\u0628\u0639\u0629',
      loading: '\u062c\u0627\u0631\u064d \u0627\u0644\u062a\u062d\u0645\u064a\u0644...',
      welcome: '\u0645\u0631\u062d\u0628\u0627\u064b',
      enterPwd: '\u0623\u062f\u062e\u0644 \u0643\u0644\u0645\u0629 \u0627\u0644\u0645\u0631\u0648\u0631 \u0644\u0644\u0645\u062a\u0627\u0628\u0639\u0629',
      footer: '\u062c\u0627\u0645\u0639\u0629 \u0643\u0627\u0631\u0627\u0628\u0648\u0643 \u2014 \u0643\u0644\u064a\u0629 \u0627\u0644\u0625\u0644\u0647\u064a\u0627\u062a',
    },
    tr: {
      title: 'Giri\u015f Yap',
      subtitle: 'Tekrar ho\u015f geldin, \u00f6\u011frenme yolculu\u011funa devam et',
      email: 'E-posta',
      password: '\u015eifre',
      name: 'Ad Soyad',
      year: 'S\u0131n\u0131f',
      login: 'Giri\u015f Yap',
      signup: 'Yeni hesap olu\u015ftur',
      guest: 'Misafir olarak g\u00f6zat',
      back: '\u2190 Geri',
      checking: 'Kontrol ediliyor...',
      newAccount: 'Yeni Hesap',
      newSub: 'Bilgilerinizi tamamlay\u0131n',
      hint: 'E-postan\u0131z\u0131 girin ve Tab veya Enter bas\u0131n',
      loading: 'Y\u00fckleniyor...',
      welcome: 'Ho\u015f geldin',
      enterPwd: '\u015eifrenizi girin',
      footer: 'Karab\u00fck \u00dcniversitesi \u2014 \u0130lahiyat Fak\u00fcltesi',
    },
  }
  const t = langText[lang]"""
    login = login.replace(old_nav, new_nav)

    # أضف مبدل اللغة + زر العودة في بداية لوحة النموذج
    old_form_panel = "{/* Mobile logo */}"
    lang_switcher = """{/* Back + Language Switch */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 }}>
          <Link to="/landing" style={{
            fontSize: 13, color: 'var(--aq-text-muted)', textDecoration: 'none',
            fontFamily: lang === 'ar' ? "var(--aq-font-arabic)" : "var(--aq-font-sans)",
            transition: 'color .2s',
          }}
            onMouseEnter={e => e.currentTarget.style.color = 'var(--aq-navy)'}
            onMouseLeave={e => e.currentTarget.style.color = 'var(--aq-text-muted)'}
          >{t.back}</Link>
          <div className="langSw" style={{
            display: 'inline-flex', borderRadius: 999, border: '1px solid var(--aq-border)',
            background: 'var(--aq-card)', padding: 3, fontSize: 13, fontWeight: 500,
            boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
          }}>
            <button type="button" onClick={() => setLang('ar')}
              style={{
                borderRadius: 999, padding: '6px 14px', border: 'none', cursor: 'pointer',
                transition: 'all .2s', fontFamily: "var(--aq-font-arabic)",
                background: lang === 'ar' ? 'var(--aq-navy)' : 'transparent',
                color: lang === 'ar' ? '#FAF8F3' : 'var(--aq-text-muted)',
                boxShadow: lang === 'ar' ? '0 2px 6px rgba(15,32,68,0.3)' : 'none',
              }}>
              العربية
            </button>
            <button type="button" onClick={() => setLang('tr')}
              style={{
                borderRadius: 999, padding: '6px 14px', border: 'none', cursor: 'pointer',
                transition: 'all .2s', fontFamily: "var(--aq-font-sans)",
                background: lang === 'tr' ? 'var(--aq-navy)' : 'transparent',
                color: lang === 'tr' ? '#FAF8F3' : 'var(--aq-text-muted)',
                boxShadow: lang === 'tr' ? '0 2px 6px rgba(15,32,68,0.3)' : 'none',
              }}>
              T\u00fcrk\u00e7e
            </button>
          </div>
        </div>

        {/* Mobile logo */}"""
    login = login.replace(old_form_panel, lang_switcher)

    # استبدل النصوص الثابتة بمتغيرات اللغة
    replacements = [
        ("'تسجيل الدخول'}", "t.title}"),
        ("'جارٍ التحقق...'}", "t.checking}"),
        ("مرحباً {existingName}!", "{t.welcome} {existingName}!"),
        ("أدخل كلمة المرور للمتابعة", "{t.enterPwd}"),
        ("حساب جديد", "{t.newAccount}"),
        ("أكمل بياناتك لبدء رحلة التعلّم", "{t.newSub}"),
        ("أدخل بريدك الإلكتروني للبدء", "{t.subtitle}"),
        (">البريد الإلكتروني<", ">{t.email}<"),
        (">كلمة المرور<", ">{t.password}<"),
        (">الاسم الكامل<", ">{t.name}<"),
        (">السنة الدراسية<", ">{t.year}<"),
        ("'تسجيل الدخول ←'", "t.login + ' \\u2190'"),
        ("'إنشاء الحساب ←'", "t.signup + ' \\u2190'"),
        ("تصفّح كضيف بدون تسجيل", "{t.guest}"),
        ("أدخل بريدك واضغط Tab أو Enter للمتابعة", "{t.hint}"),
        ("جارٍ التحميل...", "{t.loading}"),
        ("جامعة كارابوك — كلية الإلهيات", "{t.footer}"),
    ]
    for old, new in replacements:
        if old in login:
            login = login.replace(old, new)

    # أضف dir ديناميكي للصفحة
    login = login.replace(
        "direction: 'rtl'",
        "direction: lang === 'ar' ? 'rtl' : 'ltr'"
    )

    open(LOGIN_PATH, "w", encoding="utf-8").write(login)
    print("✓ 2. أُضيف مبدل اللغة + ترجمات AR/TR")
else:
    print("✓ 2. مبدل اللغة موجود مسبقاً")

print("\n✅ تم! انشري بـ: vercel --prod --yes")