import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PATH = r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages\Exercises.jsx"
content = open(PATH, encoding="utf-8").read()

# الكود القديم: الزائر يحصل دائما على false
old = """    if (isGuest) {
      // Guest: check locally without saving to DB
      setShowLoginHint(true)
      setResult({ is_correct: false, correct_answer: exercise.correct_answer || '', points_earned: 0 })
      onAnswer({ is_correct: false, points_earned: 0 })
      return
    }"""

# الكود الجديد: تحقق محلي حقيقي (بنفس منطق الخادم: إزالة التشكيل والمقارنة)
new = """    if (isGuest) {
      // Guest: real local check (same normalize logic as backend), no DB save
      const normalize = (s) => (s || '').trim().toLowerCase()
        .split('').filter(c => !(c >= '\\u064B' && c <= '\\u065F') && c !== '\\u0640').join('').trim()
      const ok = normalize(value) === normalize(exercise.correct_answer)
      setShowLoginHint(true)
      setResult({ is_correct: ok, correct_answer: exercise.correct_answer || '', points_earned: 0 })
      onAnswer({ is_correct: ok, points_earned: 0 })
      return
    }"""

if old in content:
    content = content.replace(old, new)
    open(PATH, "w", encoding="utf-8").write(content)
    print("✅ تم إصلاح وضع الزائر: تصحيح محلي حقيقي بدون حفظ")
else:
    print("⚠️ لم يُعثر على الكود المتوقع — لم يتغير شيء (الملف آمن)")