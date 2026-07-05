import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PATH = r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages\LoginRegister.jsx"
content = open(PATH, encoding="utf-8").read()
fixes = 0

# ── إصلاح 1: رسالة الخطأ 422 (سبب الصفحة البيضاء) ──
old1 = "setError(err.response?.data?.detail || 'حدث خطأ، حاول مجدداً')"
new1 = """const d = err.response?.data?.detail
      setError(typeof d === 'string' ? d : 'تأكد من البريد وكلمة المرور (6 أحرف على الأقل)')"""
if old1 in content:
    content = content.replace(old1, new1)
    fixes += 1
    print("✓ إصلاح 1: معالجة خطأ 422 (الصفحة البيضاء)")

# ── إصلاح 2: منع الإرسال قبل ظهور كلمة المرور ──
old2 = """const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)"""
new2 = """const handleSubmit = async (e) => {
    e.preventDefault()
    // إن ضغط المستخدم Enter قبل فحص البريد: افحصه أولا وأظهر حقل كلمة المرور
    if (emailState === 'idle' || emailState === 'checking') {
      await handleEmailBlur()
      return
    }
    if (!password || password.length < 6) {
      setError('أدخل كلمة مرور من 6 أحرف على الأقل')
      return
    }
    setSubmitting(true)"""
if old2 in content:
    content = content.replace(old2, new2)
    fixes += 1
    print("✓ إصلاح 2: منع الإرسال بدون كلمة مرور + فحص البريد عند Enter")

if fixes == 2:
    open(PATH, "w", encoding="utf-8").write(content)
    print(f"\n✅ تم حفظ الإصلاحين بنجاح")
else:
    print(f"\n⚠️ طُبّق {fixes} من 2 فقط — لم يُحفظ شيء (الملف آمن)")